'''
cloudimage: Get Cloud Image from Internet
'''
from io       import BytesIO
from datetime import datetime, timedelta
from pytz     import timezone
from PIL      import Image
try:
    from urllib.request import urlopen
except:
    from urllib2        import urlopen

class NoCloudImageError(BaseException):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return "No Cloud Image: {}.".format(self.msg)


class CloudImage():
    '''Cloud Image API Class'''
    def __init__(self, ciinfo = '', latestapi = None, timeapi = None):
        self.ciinfo = ciinfo
        if type(latestapi) == str:
            self.latestapi = {'url': latestapi}
        else:
            self.latestapi = latestapi
        if type(timeapi) == str:
            self.timeapi = {'url': timeapi}
        else:
            self.timeapi = timeapi

    def getlatest(self, size = None, delwatermark = True):
        if self.latestapi:
            try:
                bytepic = urlopen(self.latestapi['url']).read()
            except:
                raise NoCloudImageError("Latest {} Image".format(self.ciinfo))
            byteobj = BytesIO()
            byteobj.write(bytepic)
            try:
                img = Image.open(byteobj)
            except:
                raise NoCloudImageError("Latest {} Image".format(self.ciinfo))
            if 'crop' in self.latestapi.keys():
                img = img.crop(self.latestapi['crop'])
            if 'del' in self.latestapi.keys() and delwatermark:
                for delinf in self.latestapi['del']:
                    img.paste(delinf[0], delinf[1])
            if size:
                return img.resize(size, Image.ANTIALIAS)
            elif 'size' in self.latestapi.keys():
                return img.resize(self.latestapi['size'], Image.ANTIALIAS)
            else:
                return img
        else:
            raise NoCloudImageError("Latest {} Image".format(self.ciinfo))
    
    def gettime(self, itime, size = None):
        errtimestr = itime.strftime("%Y-%m-%d %H:%M:%S")
        if self.timeapi:
            apiarg = self.timeapi.keys()
            if 'tz' in apiarg:
                time = itime.astimezone(self.timeapi['tz'])
            else:
                time = itime
            apitimestr = time.strftime("%Y%m%d%H%M")
            if 'url' in apiarg:
                apiurl = self.timeapi['url']
            else:
                raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo))
            urlstr = apiurl
            urlstr = urlstr.replace("{CC}", apitimestr[ 0: 2])
            urlstr = urlstr.replace("{YY}", apitimestr[ 2: 4])
            urlstr = urlstr.replace("{mm}", apitimestr[ 4: 6])
            urlstr = urlstr.replace("{dd}", apitimestr[ 6: 8])
            urlstr = urlstr.replace("{HH}", apitimestr[ 8:10])
            urlstr = urlstr.replace("{MM}", apitimestr[10:12])
            if 'tdt' in apiarg:
                endtime    = time + self.timeapi['tdt']
                endtimestr = endtime.strftime("%Y%m%d%H%M%S")
                urlstr = urlstr.replace("{C2}", endtimestr[ 0: 2])
                urlstr = urlstr.replace("{Y2}", endtimestr[ 2: 4])
                urlstr = urlstr.replace("{m2}", endtimestr[ 4: 6])
                urlstr = urlstr.replace("{d2}", endtimestr[ 6: 8])
                urlstr = urlstr.replace("{H2}", endtimestr[ 8:10])
                urlstr = urlstr.replace("{M2}", endtimestr[10:12])
            try:
                bytepic = urlopen(urlstr).read()
            except:
                raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo)+urlstr)
            byteobj = BytesIO()
            byteobj.write(bytepic)
            if size:
                try:
                    return Image.open(byteobj).resize(size, Image.ANTIALIAS)
                except:
                    raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo))
            elif 'size' in self.latestapi.keys():
                try:
                    return Image.open(byteobj).resize(self.timeapi['size'], Image.ANTIALIAS)
                except:
                    raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo))
            else:
                try:
                    return Image.open(byteobj)
                except:
                    raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo))
            
        else:
            raise NoCloudImageError("{} {} Image".format(errtimestr, self.ciinfo))


FY4A_DISK_430 = CloudImage(
    ciinfo    = '430 x 430 FengYun 4A Full Disk',
    latestapi = {'url': 'http://nsmc.org.cn/NSMC/focusimg/SEVP_FY4A_DISK.JPG',
                 'del': [('black', (  0,   0,  85,  30)),
                         ('black', (395, 395, 430, 430))]}
)

FY4A_DISK_2198 = CloudImage(
    ciinfo    = '2198 x 2198 FengYun 4A Full Disk',
    latestapi = {'url' : 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG',
                 'del': [('black', (   0,    0,  430,  160)),
                         ('black', (2000, 2000, 2198, 2198))]}
)

FY4A_DISK_HF_2748 = CloudImage(
    ciinfo    = '2748 x 2748 FengYun 4A Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/china_fy4/latest.jpg',
                 'del': [('black', (0, 0, 614, 144)),
                         ('black', (0, 0, 550, 287))]}
)

FY4A_CHINA_430_268 = CloudImage(
    ciinfo    = '430 x 268 FengYun 4A China',
    latestapi = {'url': 'http://nsmc.org.cn/NSMC/focusimg/SEVP_FY4A_CHINA.JPG'}
)

FY4A_CHINA_1965_1225 = CloudImage(
    ciinfo    = '1965 x 1225 FengYun 4A China',
    latestapi = {'url': 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_CHINA.JPG'}
)

FY2F_NWPACIFIC_IR1GRAY_1000 = CloudImage(
    ciinfo    = '1000 x 1000 FengYun 2F Northwest Pacific Ocean IR1 Gray',
    latestapi = {'url': 'http://img.nsmc.org.cn/CLOUDIMAGE/FY2F/REG/FY2F_SEC_IR1_PA5_YYYYMMDD_HHmm.jpg'}
)

FY2H_SILKROAD_GRAY_HF_2000_1200 = CloudImage(
    ciinfo    = '2000 x 1200 FengYun 2H Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/china_fy2/latest.jpg'}
)

FY_SUN_HALPHA_430 = CloudImage(
    ciinfo    = '430 x 430 FengYun Sun Hα',
    latestapi = {'url': 'http://nsmc.org.cn/NSMC/focusimg/ThumSEVP_NSMC_SOHA_NCSW_ESWE_AGLB_LNO_P9_YYYYMMDDTTmm00000.jpg',
                 'del': [('black', (0, 20, 65, 42))]}
)

FY_SUN_HALPHA_1108 = CloudImage(
    ciinfo    = '1108 x 1108 FengYun Sun Hα',
    latestapi = {'url': 'http://img.nsmc.org.cn/spaceimg/SEVP_NSMC_SOHA_NCSW_ESWE_AGLB_LNO_P9_YYYYMMDDTTmm00000.JPG',
                 'del': [('black', (0, 60, 155, 110))]}
)

CHINA_RADAR_HF_1024_880 = CloudImage(
    ciinfo    = '1024 x 880 China Radar from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/radar/china/latest.png',
                 'del': [('white', (1, 1, 263, 74))]}
)

FY4A_DISK      = FY4A_DISK_2198
FY4A_DISK_HF   = FY4A_DISK_HF_2748
FY2F_NWPACIFIC = FY2F_NWPACIFIC_IR1GRAY_1000
FY2H_SILKROAD  = FY2H_SILKROAD_GRAY_HF_2000_1200
FY_SUN_HALPHA  = FY_SUN_HALPHA_1108
CHINA_RADAR    = CHINA_RADAR_HF_1024_880


Himawari8_DISK_DT_11000 = CloudImage(
    ciinfo    = '11000 x 11000 Himawari 8 Full Disk from Digital Typhoon',
    latestapi = {'url': 'http://agora.ex.nii.ac.jp/digital-typhoon/himawari-3g/latest/Hsfd/full/latest.jpg',
                 'del': [('black', (   0,     0,  3300,   385)),
                         ('black', (7557,     0, 11000,   352)),
                         ('black', (   0, 10560,  2530, 11000)),
                         ('black', (9757, 10604, 11000, 11000))]}
)

Himawari8_DISK_DT_1000 = CloudImage(
    ciinfo    = '1000 x 1000 Himawari 8 Full Disk from Digital Typhoon',
    latestapi = {'url': 'http://agora.ex.nii.ac.jp/digital-typhoon/himawari-3g/latest/Hsfd/RGB/latest.jpg',
                 'del': [('black', (  0,   0,  300,   35)),
                         ('black', (687,   0, 1000,   32)),
                         ('black', (  0, 960,  230, 1000)),
                         ('black', (887, 964, 1000, 1000))]}
)

Himawari8_DISK_IR_DT_512 = CloudImage(
    ciinfo    = '512 x 512 Himawari 8 Full Disk IR from Digital Typhoon',
    latestapi = {'url': 'http://agora.ex.nii.ac.jp/digital-typhoon/latest/globe/512x512/ir.jpg',
                 'del': [('black', (  0,   0, 120,  32)),
                         ('black', (  0, 492,  75, 512)),
                         ('black', (431, 478, 512, 512)),
                         ('black', (354, 495, 512, 512))]}
)

Himawari8_DISK_IR_DT_2048 = CloudImage(
    ciinfo    = '2048 x 2048 Himawari 8 Full Disk IR from Digital Typhoon',
    latestapi = {'url': 'http://agora.ex.nii.ac.jp/digital-typhoon/latest/globe/2048x2048/ir.jpg',
                 'del': [('black', (   0,    0,  480,  128)),
                         ('black', (   0, 1968,  300, 2048)),
                         ('black', (1724, 1912, 2048, 2048)),
                         ('black', (1416, 1980, 2048, 2048))]}
)

Himawari8_DISK_WALLPAPER_DT_1024_768 = CloudImage(
    ciinfo    = '1024 x 768 Himawari 8 Full Disk Wallpaper from Digital Typhoon',
    latestapi = {'url': 'http://agora.ex.nii.ac.jp/digital-typhoon/wallpaper/globe/1024x768/latest.jpg',
                 'del': [('black', (  0,   0,  296,  49)),
                         ('black', (  0, 717,  270, 768)),
                         ('black', (863, 715, 1024, 768)),
                         ('black', (618, 740, 1024, 768))]}
)

Himawari8_DISK_HF_1024 = CloudImage(
    ciinfo    = '1024 x 1024 Himawari 8 Full Disk from HeFeng weather website',
    latestapi = {'url' : 'https://imagery.heweather.net/imagery/satellite/japan/latest.png',
                 'crop': (0, 0, 1024, 1024),
                 'del' : [('black', (0, 1021, 1024, 1024))]}
)

JAPAN_RADAR_HF_600_522 = CloudImage(
    ciinfo    = '600 x 522 Japan Radar from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/radar/japan/latest.png'}
)

Himawari8_DISK    = Himawari8_DISK_DT_1000
Himawari8_DISK_IR = Himawari8_DISK_IR_DT_2048
Himawari8_DISK_HF = Himawari8_DISK_HF_1024
Himawari8_DISK_WP = Himawari8_DISK_WALLPAPER_DT_1024_768
JAPAN_RADAR       = JAPAN_RADAR_HF_600_522


GEOS_16_DISK_HF_339 = CloudImage(
    ciinfo    = '339 x 339 GEOS-16 Full Disk from HeFeng weather website',
    latestapi = {'url' : 'https://imagery.heweather.net/imagery/satellite/us_east/small/latest.jpg',
                 'crop': (0, 0, 339, 323),
                 'size': (339, 339)}
)

GEOS_16_DISK_HF_1808 = CloudImage(
    ciinfo    = '1808 x 1808 GEOS-16 Full Disk from HeFeng weather website',
    latestapi = {'url' : 'https://imagery.heweather.net/imagery/satellite/us_east/large/latest.jpg',
                 'del' : [('black', (0, 1611, 167, 1776))],
                 'crop': (0, 0, 1808, 1776),
                 'size': (1808, 1808)}
)

GEOS_17_DISK_HF_339 = CloudImage(
    ciinfo    = '339 x 339 GEOS-17 Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/us_west/small/latest.jpg',
                 'crop': (0, 0, 339, 323),
                 'size': (339, 339)}
)

GEOS_17_DISK_HF_1808 = CloudImage(
    ciinfo    = '1808 x 1808 GEOS-17 Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/us_west/large/latest.jpg',
                 'del' : [('black', (0, 1611, 167, 1776))],
                 'crop': (0, 0, 1808, 1776),
                 'size': (1808, 1808)}
)

USA_RADAR_HF_640_480 = CloudImage(
    ciinfo    = '640 x 480 USA Radar from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/radar/us/latest.png'}
)

GEOS_16_DISK = GEOS_16_DISK_HF_1808
GEOS_17_DISK = GEOS_17_DISK_HF_1808
USA_RADAR    = USA_RADAR_HF_640_480


Meteosat8_DISK_HF_800 = CloudImage(
    ciinfo    = '800 x 800 Meteosat 8 (Meteosat IODC) Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/europe_41p5/latest.png'}
)

Meteosat11_DISK_HF_800 = CloudImage(
    ciinfo    = '800 x 800 Meteosat 11 (Meteosat 0deg) Full Disk from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/satellite/europe_0/latest.png'}
)

EUROPE_RADAR_HF_3196_4000 = CloudImage(
    ciinfo    = '3196 x 4000 Europe Radar from HeFeng weather website',
    latestapi = {'url': 'https://imagery.heweather.net/imagery/radar/europe/latest.png',
                 'del': [((0, 0, 0, 112), (64, 3715, 294, 3920))]}
)

Meteosat_IODC = Meteosat8_DISK  = Meteosat8_DISK_HF_800
Meteosat_0deg = Meteosat11_DISK = Meteosat11_DISK_HF_800
EUROPE_RADAR  = EUROPE_RADAR_HF_3196_4000

