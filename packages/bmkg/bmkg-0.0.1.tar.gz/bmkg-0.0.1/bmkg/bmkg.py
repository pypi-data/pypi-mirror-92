import aiohttp
from xmltodict import parse
from .weather import Weather
from .constants import PROVINCES
from .earthquake import Earthquake, EarthquakeFelt, TsunamiEarthquake
from datetime import datetime

class BMKG:
    def __repr__(self):
        return f"<BMKG english={self.english} metric={self.metric}>"

    def __init__(self, english: bool = False, metric: bool = True, session = None, session_settings: dict = {}) -> None:
        """
        BMKG wrapper for Python.
        """
        
        self.english = bool(english)
        self.metric = bool(metric)
        self.session = session or aiohttp.ClientSession(**session_settings)
        self.base_url = "https://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/"
        self._day = self._current_day()
        self._image_cache = {}
    
    def _current_day(self):
        current = datetime.now()
        return f"{current.year}{current.month}{current.day}"
    
    async def get_forecast(self, location: str = None):
        if not location:
            return await self._handle_request(PROVINCES["indonesia"])
        
        location = str(location).lower().replace(" ", "_").replace("di", "dki").replace("jogja", "yogya").lstrip("provinsi ")
        if location in PROVINCES.keys():
            return await self._handle_request(PROVINCES[location])
        
        for province in PROVINCES.keys():
            if location in province:
                return await self._handle_request(PROVINCES[province])
        return await self._handle_request(PROVINCES["indonesia"])

    async def get_climate_info(self):
        if self._image_cache.get("climate_info") and (self._current_day() == self._day):
            return self._image_cache["climate_info"]
        
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/CEWS/pch/pch.bulan.1.cond1.png")
        byte = await response.read()
        self._image_cache["climate_info"] = byte
        return byte
    
    async def get_satellite_image(self):
        if self._image_cache.get("satellite") and (self._current_day() == self._day):
            return self._image_cache["satellite"]
        
        response = await self.session.get("https://inderaja.bmkg.go.id/IMAGE/HIMA/H08_EH_Indonesia.png")
        byte = await response.read()
        self._image_cache["satellite"] = byte
        return byte
    
    async def get_wave_height_forecast(self):
        if self._image_cache.get("wave_height") and (self._current_day() == self._day):
            return self._image_cache["wave_height"]
        
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/maritim/gelombang_maritim.png")
        byte = await response.read()
        self._image_cache["wave_height"] = byte
        return byte

    async def get_wind_forecast(self):
        if self._image_cache.get("wind_forecast") and (self._current_day() == self._day):
            return self._image_cache["wind_forecast"]
        
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/angin/streamline_d1.jpg")
        byte = await response.read()
        self._image_cache["wind_forecast"] = byte
        return byte
    
    async def get_forest_fires(self):
        if self._image_cache.get("forest_fires") and (self._current_day() == self._day):
            return self._image_cache["forest_fires"]
        
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/spartan/36_indonesia_ffmc_01.png")
        byte = await response.read()
        self._image_cache["forest_fires"] = byte
        return byte
    
    async def get_recent_earthquake_map(self):
        if self._image_cache.get("latest_earthquake") and (self._current_day() == self._day):
            return self._image_cache["latest_earthquake"]
        
        response = await self.session.get("https://data.bmkg.go.id/eqmap.gif")
        byte = await response.read()
        self._image_cache["latest_earthquake"] = byte
        return byte

    async def get_recent_earthquake(self):
        response = await self.session.get("https://data.bmkg.go.id/gempaterkini.xml")
        text = await response.text()
        return Earthquake(text, metric=self.metric)
    
    async def get_recent_tsunami(self):
        response = await self.session.get("https://data.bmkg.go.id/lasttsunami.xml")
        text = await response.text()
        return TsunamiEarthquake(text, metric=self.metric)
    
    async def get_earthquakes_felt(self):
        response = await self.session.get("https://data.bmkg.go.id/gempadirasakan.xml")
        text = await response.text()
        result = parse(text)["Infogempa"]
        earthquakes = []
        
        for earthquake in result["Gempa"]:
            earthquakes.append(EarthquakeFelt(earthquake, metric=self.metric))
        return earthquakes

    async def get_recent_earthquakes(self):
        response = await self.session.get("https://data.bmkg.go.id/gempaterkini.xml")
        text = await response.text()
        result = parse(text)["Infogempa"]
        earthquakes = []
        
        for earthquake in result["gempa"]:
            earthquakes.append(Earthquake(earthquake, as_list_element=True, metric=self.metric))
        return earthquakes

    async def _handle_request(self, xml_path: str):
        response = await self.session.get(self.base_url + xml_path)
        text = await response.text()
        return Weather(text, english=self.english, metric=self.metric)
    
    async def close(self):
        await self.session.close()
        del (
            self._day,
            self.base_url,
            self.session,
            self.english,
            self.metric,
            self._image_cache
        )