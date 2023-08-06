def isinpolygon(point, vertex_lst, contain_boundary=True):
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis), max(lngaxis)
    minlat, maxlat = min(lataxis), max(lataxis)
    lng, lat = point
    if contain_boundary:
        isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
    else:
        isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
    return isin


def isintersect( poi, spoi, epoi):
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        return None
    if slat == elat:
        return False
    if slat > lat and elat > lat:
        return False
    if slat < lat and elat < lat:
        return False
    if slat == lat and elat > lat:
        return False
    if elat == lat and slat > lat:
        return False
    if slng < lng and elat < lat:
        return False
    xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
    if xseg == lng:
        return None
    if xseg < lng:
        return False
    return True