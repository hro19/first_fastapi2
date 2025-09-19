from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Set
from pydantic import BaseModel, Field
import httpx
import asyncio
from collections import defaultdict

router = APIRouter()

class CitiesResponse(BaseModel):
    prefecture: str = Field(..., description="都道府県名")
    cities: List[str] = Field(..., description="市一覧")
    wards: List[str] = Field(..., description="区一覧")
    towns: List[str] = Field(..., description="町一覧")
    villages: List[str] = Field(..., description="村一覧")
    total_count: int = Field(..., description="総数")

class PrefecturesResponse(BaseModel):
    prefectures: List[str] = Field(..., description="都道府県一覧")
    count: int = Field(..., description="都道府県数")

class HealthResponse(BaseModel):
    status: str = Field(..., description="ステータス")
    loaded_prefectures: int = Field(..., description="読み込み済み都道府県数")

class JapaneseCityAPI:
    def __init__(self):
        self.address_data = None
        self.cities_by_prefecture = defaultdict(set)
        self.is_loaded = False
    
    async def load_address_data(self):
        """Geoloniaの住所データを取得・加工"""
        if self.is_loaded:
            return
            
        try:
            # Geoloniaの住所データURL（リポジトリのデフォルトブランチは master ）
            url = "https://raw.githubusercontent.com/geolonia/japanese-addresses/master/api/ja.json"
            
            print(f"Loading address data from: {url}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                
                if response.status_code == 200:
                    self.address_data = response.json()
                    print(f"Successfully loaded data. Keys count: {len(self.address_data) if self.address_data else 0}")
                    self._process_address_data()
                    print(f"Processed prefectures: {len(self.cities_by_prefecture)}")
                    self.is_loaded = True
                else:
                    print(f"Failed to load address data: {response.status_code}")
                    self._load_fallback_data()
        except Exception as e:
            print(f"Error loading address data: {e}")
            self._load_fallback_data()
    
    def _process_address_data(self):
        """住所データを処理して都道府県別の市区町村リストを作成"""
        if not self.address_data:
            return
        
        # Geolonia APIのデータ形式: {"都道府県名": ["市区町村名", ...], ...}
        for prefecture, cities in self.address_data.items():
            if prefecture and cities:
                for city in cities:
                    if city:
                        self.cities_by_prefecture[prefecture].add(city)
    
    def _load_fallback_data(self):
        """フォールバック用の静的データ"""
        print("Loading fallback data...")
        fallback_data = {
            '神奈川県': [
                '横浜市', '川崎市', '相模原市', '横須賀市', '平塚市', '鎌倉市',
                '藤沢市', '小田原市', '茅ヶ崎市', '逗子市', '三浦市', '秦野市',
                '厚木市', '大和市', '伊勢原市', '海老名市', '座間市', '南足柄市',
                '綾瀬市', '葉山町', '寒川町', '大磯町', '二宮町', '中井町',
                '大井町', '松田町', '山北町', '開成町', '箱根町', '真鶴町',
                '湯河原町', '愛川町', '清川村'
            ],
            '東京都': [
                '千代田区', '中央区', '港区', '新宿区', '文京区', '台東区',
                '墨田区', '江東区', '品川区', '目黒区', '大田区', '世田谷区',
                '渋谷区', '中野区', '杉並区', '豊島区', '北区', '荒川区',
                '板橋区', '練馬区', '足立区', '葛飾区', '江戸川区',
                '八王子市', '立川市', '武蔵野市', '三鷹市', '青梅市', '府中市',
                '昭島市', '調布市', '町田市', '小金井市', '小平市', '日野市',
                '東村山市', '国分寺市', '国立市', '福生市', '狛江市', '東大和市',
                '清瀬市', '東久留米市', '武蔵村山市', '多摩市', '稲城市', '羽村市',
                'あきる野市', '西東京市'
            ],
            '大阪府': [
                '大阪市', '堺市', '岸和田市', '豊中市', '池田市', '吹田市',
                '泉大津市', '高槻市', '貝塚市', '守口市', '枚方市', '茨木市',
                '八尾市', '泉佐野市', '富田林市', '寝屋川市', '河内長野市',
                '松原市', '大東市', '和泉市', '箕面市', '柏原市', '羽曳野市',
                '門真市', '摂津市', '高石市', '藤井寺市', '東大阪市', '泉南市',
                '四條畷市', '交野市', '大阪狭山市', '阪南市'
            ]
        }
        
        for prefecture, cities in fallback_data.items():
            self.cities_by_prefecture[prefecture] = set(cities)
        
        print(f"Fallback data loaded: {len(self.cities_by_prefecture)} prefectures")
        self.is_loaded = True
    
    def _normalize_prefecture_name(self, prefecture_name: str) -> str:
        """入力値を公式な都道府県名に揃える"""
        if not prefecture_name:
            return prefecture_name

        # 既に正式名称ならそのまま返す
        if prefecture_name in self.cities_by_prefecture:
            return prefecture_name

        # データ読み込み前の場合に備え、特殊ケースを先に処理
        special_cases = {
            '北海道': '北海道',
            '東京': '東京都',
            '大阪': '大阪府',
            '京都': '京都府'
        }
        if prefecture_name in special_cases:
            return special_cases[prefecture_name]

        # 読み込み済みデータから「県/府/都」抜きの表記をマップ化
        normalized_map = {}
        for official_name in self.cities_by_prefecture.keys():
            if official_name.endswith(('都', '府', '県')):
                normalized_map[official_name[:-1]] = official_name
            else:
                normalized_map[official_name] = official_name

        if prefecture_name in normalized_map:
            return normalized_map[prefecture_name]

        # サフィックスを付けたバリエーションを試す
        for suffix in ('県', '府', '都', '道'):
            candidate = prefecture_name + suffix
            if candidate in self.cities_by_prefecture:
                return candidate

        return prefecture_name

    def get_cities_by_prefecture(self, prefecture_name: str) -> Dict[str, Any]:
        """都道府県名から市区町村一覧を取得"""
        prefecture_name = self._normalize_prefecture_name(prefecture_name)

        cities = list(self.cities_by_prefecture.get(prefecture_name, set()))

        # 市・区を分離
        cities_data = self._categorize_cities(cities)
        
        return {
            'prefecture': prefecture_name,
            'cities': sorted(cities_data['cities']),
            'wards': sorted(cities_data['wards']),
            'towns': sorted(cities_data['towns']),
            'villages': sorted(cities_data['villages']),
            'total_count': len(cities)
        }
    
    def _categorize_cities(self, cities: List[str]) -> Dict[str, List[str]]:
        """市区町村を種別に分類"""
        result = {
            'cities': [],  # 市
            'wards': [],   # 区
            'towns': [],   # 町
            'villages': [] # 村
        }
        
        for city in cities:
            if '市' in city:
                result['cities'].append(city)
            elif '区' in city:
                result['wards'].append(city)
            elif '町' in city:
                result['towns'].append(city)
            elif '村' in city:
                result['villages'].append(city)
            else:
                result['cities'].append(city)  # デフォルトは市に分類
        
        return result
    
    def get_all_prefectures(self) -> List[str]:
        """全都道府県一覧を取得"""
        return sorted(list(self.cities_by_prefecture.keys()))

# APIインスタンス作成
city_api = JapaneseCityAPI()

@router.get("/prefectures", response_model=PrefecturesResponse)
async def get_prefectures() -> PrefecturesResponse:
    """
    全都道府県一覧を返すAPI
    
    Returns:
        PrefecturesResponse: 都道府県一覧とその数
    """
    # データが読み込まれていない場合は読み込み
    if not city_api.is_loaded:
        await city_api.load_address_data()
    
    prefectures = city_api.get_all_prefectures()
    return PrefecturesResponse(
        prefectures=prefectures,
        count=len(prefectures)
    )

@router.get("/cities/{prefecture}", response_model=CitiesResponse)
async def get_cities_by_path(prefecture: str) -> CitiesResponse:
    """
    指定された都道府県の市区町村一覧を返すAPI（パスパラメータ版）
    
    Args:
        prefecture: 都道府県名
        
    Returns:
        CitiesResponse: 市区町村一覧
        
    Examples:
        GET /basic/cities/神奈川
        GET /basic/cities/東京
    """
    # データが読み込まれていない場合は読み込み
    if not city_api.is_loaded:
        await city_api.load_address_data()
    
    result = city_api.get_cities_by_prefecture(prefecture)
    
    if result['total_count'] == 0:
        available_prefectures = city_api.get_all_prefectures()
        raise HTTPException(
            status_code=404,
            detail={
                'error': f'都道府県 "{prefecture}" が見つかりませんでした',
                'available_prefectures': available_prefectures
            }
        )
    
    return CitiesResponse(**result)

@router.get("/cities", response_model=CitiesResponse)
async def get_cities_by_query(
    prefecture: str = Query(..., description="都道府県名（例: 神奈川、東京、大阪）")
) -> CitiesResponse:
    """
    クエリパラメータで都道府県を指定して市区町村一覧を取得
    
    Args:
        prefecture: 都道府県名
        
    Returns:
        CitiesResponse: 市区町村一覧
        
    Examples:
        GET /basic/cities?prefecture=神奈川
        GET /basic/cities?prefecture=東京
    """
    # データが読み込まれていない場合は読み込み
    if not city_api.is_loaded:
        await city_api.load_address_data()
    
    result = city_api.get_cities_by_prefecture(prefecture)
    
    if result['total_count'] == 0:
        available_prefectures = city_api.get_all_prefectures()
        raise HTTPException(
            status_code=404,
            detail={
                'error': f'都道府県 "{prefecture}" が見つかりませんでした',
                'available_prefectures': available_prefectures
            }
        )
    
    return CitiesResponse(**result)

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    ヘルスチェック用エンドポイント
    
    Returns:
        HealthResponse: システムの健康状態
    """
    # データが読み込まれていない場合は読み込み
    if not city_api.is_loaded:
        await city_api.load_address_data()
    
    return HealthResponse(
        status="healthy",
        loaded_prefectures=len(city_api.cities_by_prefecture)
    )
