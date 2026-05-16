import pandas as pd

today = pd.Timestamp.now()

# Weather data for location: https://maps.app.goo.gl/Wmndhb642E37jSKu7
url = f"""
    https://api.open-meteo.com/v1/forecast
    ?   latitude        =   50.029498
    &   longitude       =   19.906195
    &   daily           =   temperature_2m_max
    &   timezone        =   auto
    &   past_days       =   {today.day-1}
    &   forecast_days   =   1
"""
data = pd.read_json("".join(url.split()))

data_series = pd.Series(
    data.daily.temperature_2m_max, 
    index = data.daily.time, 
    name = "Maximum temperature at 2 m"
    )

print(data_series)

"""
Example:

2026-05-01    18.3                                                                                                                                                                         
2026-05-02    21.5
2026-05-03    25.0
2026-05-04    27.0
2026-05-05    27.5
2026-05-06    26.3
2026-05-07    21.7
2026-05-08    15.6
2026-05-09    15.8
2026-05-10    19.9
2026-05-11    22.7
2026-05-12    13.3
2026-05-13    14.2
2026-05-14    18.0
2026-05-15    16.3
2026-05-16    12.1
Name: Maximum temperature at 2 m, dtype: float64
"""