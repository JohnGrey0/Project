import os
from PIL import Image, ExifTags
import pytesseract
import csv
import re
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config = ('-l eng --oem 1 --psm 3')

custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789F°'

def convert_exif_datetime(exif_date_time: str) -> str:
    """
    Converts a date-time string from EXIF format 'YYYY:MM:DD HH:MM:SS' 
    to standard format 'YYYY-MM-DD HH:MM:SS'.
    
    Args:
    exif_date_time (str): The date-time string in EXIF format.

    Returns:
    str: The converted date-time string in standard format.
    """
    try:
        # Convert the EXIF date-time to standard format
        converted_date_time = datetime.strptime(exif_date_time, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        return converted_date_time
    except ValueError as e:
        print(f"Error converting date-time: {e}")
        return None  # Return None if the format is incorrect

def get_exif_data(img):
    exif_data = img._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            decoded_tag = ExifTags.TAGS.get(tag, tag)
            # if tag in ExifTags.TAGS:
            #     print(f'{ExifTags.TAGS[tag]}:{value}')
            # else:
            #     print(f'{tag}:{value}')
            if decoded_tag == 'DateTimeOriginal':
                return convert_exif_datetime(value)
    return None
# Ensure Tesseract is installed and set up correctly
# For example, if using Windows, set the path to your tesseract installation:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create a CSV file to store the results if it doesn't already exist
csv_file = 'archive_data.csv'
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image Name', 'Date', 'Temp'])

# Define the directory where the images are stored
image_dir = 'archived_live_photos'

error_set = set()
track_errors = {}

for image_file in os.listdir(image_dir):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(image_dir, image_file)

        # Open the image
        with Image.open(image_path) as img:
            date = get_exif_data(img)
            # Get image dimensions
            width, height = img.size
             # 1. Crop the top 16 pixels from the image (entire width)
            top_16_crop = img.crop((0, 0, width, 16))
            
            # Crop from 100 pixels to the left of the rightmost side of the image
            crop_right = top_16_crop.crop((width-80, 0, width-45, 16))
            # if '000013' in image_file:
            # crop_right.show()
            temp = pytesseract.image_to_string(crop_right, config=custom_config)
            temp = temp.replace('°', '').replace('\r', '').replace('\n', '').replace('F', '').replace('693', '68')
            print(temp)
            error_set.add(temp)
            # if temp not in track_errors:
            #     track_errors.setdefault(temp, []).append(image_file)
            # track_errors[temp].append(image_file)
            # Combine the extracted text from all sections
            print(f"{image_file} - {temp}\n\t{error_set}")
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([image_file, date, temp])
                print(f"Extracted data from {image_file}: Date: {date}, Temp: {temp}")

# {'49', '51', '68', '69', '59', '71', '66', '67', '64', '50', '55', '7', '60', '53'}
# {'69': ['000001.jpg', '000001.jpg', '000002.jpg', '000071.jpg', '000072.jpg', '000073.jpg', '000074.jpg', '000075.jpg', '000076.jpg', '000077.jpg', '000086.jpg', '000088.jpg', '000089.jpg', '000091.jpg', '000092.jpg', '000093.jpg', '000094.jpg', '000095.jpg', '000096.jpg', '000175.jpg', '000176.jpg', '000177.jpg', '000178.jpg', '000179.jpg', '000205.jpg', '000206.jpg', '000207.jpg'], '68': ['000003.jpg', '000003.jpg', '000004.jpg', '000068.jpg', '000069.jpg', '000070.jpg', '000097.jpg', '000098.jpg', '000099.jpg', '000100.jpg', '000173.jpg', '000174.jpg', '000208.jpg', '000209.jpg', '000210.jpg', '000211.jpg', '000212.jpg', '000213.jpg', '000232.jpg'], '66': ['000005.jpg', '000005.jpg', '000006.jpg', '000007.jpg', '000008.jpg', '000009.jpg', '000066.jpg', '000067.jpg', '000101.jpg', '000102.jpg', '000103.jpg', '000104.jpg', '000105.jpg', '000107.jpg', '000171.jpg', '000172.jpg', '000214.jpg', '000215.jpg', '000216.jpg', '000217.jpg', '000218.jpg', '000219.jpg', '000220.jpg', '000221.jpg', '000224.jpg', '000225.jpg', '000226.jpg', '000227.jpg', '000228.jpg', '000229.jpg', '000230.jpg', '000231.jpg', '000299.jpg', '000300.jpg', '000301.jpg', '000302.jpg', '000303.jpg', '000304.jpg', '000305.jpg'], '64': ['000010.jpg', '000010.jpg', '000011.jpg', '000012.jpg', '000014.jpg', '000065.jpg', '000106.jpg', '000108.jpg', '000109.jpg', '000110.jpg', '000111.jpg', '000112.jpg', '000113.jpg', '000114.jpg', '000125.jpg', '000168.jpg', '000169.jpg', '000170.jpg', '000222.jpg', '000223.jpg', '000233.jpg', '000234.jpg', '000235.jpg', '000236.jpg', '000243.jpg', '000258.jpg', '000259.jpg', '000279.jpg', '000286.jpg', '000287.jpg', '000288.jpg', '000289.jpg', '000290.jpg', '000291.jpg', '000292.jpg', '000293.jpg', '000294.jpg', '000295.jpg', '000296.jpg', '000297.jpg', '000298.jpg', '000306.jpg', '000307.jpg', '000308.jpg', '000309.jpg', '000310.jpg', '000311.jpg', '000312.jpg', '000313.jpg', '000314.jpg', '000315.jpg', '000316.jpg'], '67': ['000013.jpg', '000013.jpg', '000015.jpg', '000016.jpg', '000017.jpg', '000018.jpg', '000063.jpg', '000064.jpg', '000115.jpg', '000116.jpg', '000117.jpg', '000118.jpg', '000119.jpg', '000120.jpg', '000121.jpg', '000122.jpg', '000123.jpg', '000124.jpg', '000126.jpg', '000127.jpg', '000128.jpg', '000129.jpg', '000130.jpg', '000131.jpg', '000132.jpg', '000133.jpg', '000134.jpg', '000135.jpg', '000136.jpg', '000137.jpg', '000138.jpg', '000139.jpg', '000140.jpg', '000148.jpg', '000166.jpg', '000167.jpg', '000237.jpg', '000238.jpg', '000239.jpg', '000240.jpg', '000241.jpg', '000242.jpg', '000244.jpg', '000245.jpg', '000246.jpg', '000247.jpg', '000248.jpg', '000249.jpg', '000250.jpg', '000251.jpg', '000252.jpg', '000253.jpg', '000254.jpg', '000255.jpg', '000256.jpg', '000257.jpg', '000260.jpg', '000261.jpg', '000262.jpg', '000263.jpg', '000264.jpg', '000265.jpg', '000266.jpg', '000267.jpg', '000268.jpg', '000269.jpg', '000270.jpg', '000271.jpg', '000272.jpg', '000273.jpg', '000274.jpg', '000275.jpg', '000276.jpg', '000277.jpg', '000278.jpg', '000280.jpg', '000281.jpg', '000282.jpg', '000283.jpg', '000284.jpg', '000285.jpg', '000317.jpg', '000318.jpg', '000319.jpg', '000320.jpg', '000321.jpg', '000322.jpg', '000323.jpg', '000324.jpg', '000325.jpg', '000326.jpg', '000327.jpg', '000331.jpg', '000332.jpg', '000333.jpg', '000334.jpg', '000335.jpg', '000336.jpg', '000337.jpg', '000338.jpg', '000339.jpg', '000340.jpg', '000341.jpg', '000342.jpg', '000343.jpg', '000344.jpg', '000345.jpg', '000346.jpg', '000347.jpg', '000348.jpg', '000349.jpg', '000350.jpg', '000351.jpg', '000352.jpg', '000353.jpg', '000354.jpg', '000355.jpg', '000356.jpg', '000357.jpg', '000358.jpg', '000359.jpg', '000360.jpg', '000361.jpg', '000362.jpg', '000363.jpg', '000364.jpg', '000365.jpg', '000366.jpg', '000525.jpg', '000526.jpg', '000527.jpg', '000528.jpg', '000529.jpg', '000530.jpg', '000531.jpg', '000532.jpg', '000533.jpg', '000534.jpg', '000535.jpg', '000536.jpg', '000537.jpg', '000538.jpg', '000539.jpg', '000540.jpg', '000541.jpg'], '60': ['000019.jpg', '000019.jpg', '000020.jpg', '000021.jpg', '000022.jpg', '000023.jpg', '000025.jpg', '000061.jpg', '000062.jpg', '000141.jpg', '000142.jpg', '000143.jpg', '000144.jpg', '000145.jpg', '000146.jpg', '000147.jpg', '000149.jpg', '000150.jpg', '000151.jpg', '000152.jpg', '000153.jpg', '000154.jpg', '000164.jpg', '000165.jpg', '000328.jpg', '000329.jpg', '000330.jpg', '000367.jpg', '000368.jpg', '000369.jpg', '000370.jpg', '000371.jpg', '000372.jpg', '000373.jpg', '000374.jpg', '000375.jpg', '000376.jpg', '000378.jpg', '000379.jpg', '000410.jpg', '000413.jpg', '000414.jpg', '000415.jpg', '000416.jpg', '000417.jpg', '000418.jpg', '000419.jpg', '000420.jpg', '000421.jpg', '000422.jpg', '000423.jpg', '000424.jpg', '000425.jpg', '000426.jpg', '000427.jpg', '000428.jpg', '000429.jpg', '000430.jpg', '000431.jpg', '000432.jpg', '000433.jpg', '000434.jpg', '000435.jpg', '000436.jpg', '000437.jpg', '000438.jpg', '000439.jpg', '000440.jpg', '000441.jpg', '000442.jpg', '000445.jpg', '000515.jpg', '000516.jpg', '000517.jpg', '000518.jpg', '000519.jpg', '000520.jpg', '000521.jpg', '000522.jpg', '000523.jpg', '000524.jpg', '000542.jpg', '000543.jpg', '000544.jpg', '000545.jpg', '000546.jpg', '000547.jpg', '000548.jpg', '000631.jpg', '000632.jpg', '000636.jpg', '000639.jpg', '000733.jpg', '000735.jpg', '000737.jpg'], '59': ['000024.jpg', '000024.jpg', '000026.jpg', '000027.jpg', '000028.jpg', '000029.jpg', '000060.jpg', '000155.jpg', '000156.jpg', '000157.jpg', '000158.jpg', '000159.jpg', '000160.jpg', '000161.jpg', '000162.jpg', '000163.jpg', '000377.jpg', '000380.jpg', '000381.jpg', '000382.jpg', '000383.jpg', '000384.jpg', '000385.jpg', '000386.jpg', '000387.jpg', '000388.jpg', '000389.jpg', '000390.jpg', '000391.jpg', '000392.jpg', '000393.jpg', '000394.jpg', '000395.jpg', '000396.jpg', '000397.jpg', '000398.jpg', '000399.jpg', '000400.jpg', '000401.jpg', '000402.jpg', '000403.jpg', '000404.jpg', '000405.jpg', '000406.jpg', '000407.jpg', '000408.jpg', '000409.jpg', '000411.jpg', '000412.jpg', '000443.jpg', '000444.jpg', '000446.jpg', '000447.jpg', '000448.jpg', '000449.jpg', '000450.jpg', '000451.jpg', '000452.jpg', '000453.jpg', '000454.jpg', '000455.jpg', '000456.jpg', '000457.jpg', '000458.jpg', '000459.jpg', '000460.jpg', '000461.jpg', '000462.jpg', '000463.jpg', '000464.jpg', '000465.jpg', '000466.jpg', '000467.jpg', '000469.jpg', '000512.jpg', '000513.jpg', '000514.jpg', '000549.jpg', '000550.jpg', '000551.jpg', '000552.jpg', '000553.jpg', '000618.jpg', '000619.jpg', '000620.jpg', '000621.jpg', '000622.jpg', '000623.jpg', '000624.jpg', '000625.jpg', '000626.jpg', '000627.jpg', '000628.jpg', '000629.jpg', '000630.jpg', '000633.jpg', '000634.jpg', '000635.jpg', '000637.jpg', '000638.jpg', '000640.jpg', '000641.jpg', '000642.jpg', '000643.jpg', '000644.jpg', '000645.jpg', '000646.jpg', '000648.jpg', '000650.jpg', '000716.jpg', '000717.jpg', '000718.jpg', '000719.jpg', '000720.jpg', '000721.jpg', '000722.jpg', '000723.jpg', '000724.jpg', '000725.jpg', '000726.jpg', '000727.jpg', '000728.jpg', '000729.jpg', '000730.jpg', '000731.jpg', '000732.jpg', '000734.jpg', '000736.jpg', '000738.jpg', '000739.jpg', '000740.jpg', '000741.jpg', '000742.jpg'], '7': ['000030.jpg', '000030.jpg', '000031.jpg', '000032.jpg', '000033.jpg', '000034.jpg', '000035.jpg', '000036.jpg', '000057.jpg', '000058.jpg', '000059.jpg', '000185.jpg', '000187.jpg', '000190.jpg', '000193.jpg', '000198.jpg', '000199.jpg', '000468.jpg', '000470.jpg', '000471.jpg', '000472.jpg', '000473.jpg', '000474.jpg', '000475.jpg', '000476.jpg', '000477.jpg', '000479.jpg', '000508.jpg', '000509.jpg', '000510.jpg', '000511.jpg', '000554.jpg', '000555.jpg', '000556.jpg', '000615.jpg', '000616.jpg', '000617.jpg', '000647.jpg', '000649.jpg', '000651.jpg', '000652.jpg', '000653.jpg', '000654.jpg', '000655.jpg', '000656.jpg', '000657.jpg', '000660.jpg', '000714.jpg', '000715.jpg'], '55': ['000037.jpg', '000037.jpg', '000038.jpg', '000039.jpg', '000040.jpg', '000041.jpg', '000042.jpg', '000043.jpg', '000044.jpg', '000045.jpg', '000046.jpg', '000048.jpg', '000049.jpg', '000050.jpg', '000052.jpg', '000053.jpg', '000054.jpg', '000055.jpg', '000056.jpg', '000478.jpg', '000480.jpg', '000481.jpg', '000482.jpg', '000483.jpg', '000484.jpg', '000485.jpg', '000486.jpg', '000487.jpg', '000488.jpg', '000489.jpg', '000490.jpg', '000491.jpg', '000492.jpg', '000493.jpg', '000494.jpg', '000495.jpg', '000496.jpg', '000497.jpg', '000498.jpg', '000499.jpg', '000500.jpg', '000501.jpg', '000502.jpg', '000503.jpg', '000504.jpg', '000505.jpg', '000506.jpg', '000507.jpg', '000557.jpg', '000558.jpg', '000559.jpg', '000560.jpg', '000561.jpg', '000562.jpg', '000563.jpg', '000569.jpg', '000572.jpg', '000575.jpg', '000611.jpg', '000612.jpg', '000613.jpg', '000614.jpg', '000658.jpg', '000659.jpg', '000661.jpg', '000662.jpg', '000663.jpg', '000664.jpg', '000665.jpg', '000666.jpg', '000667.jpg', '000668.jpg', '000710.jpg', '000711.jpg', '000712.jpg', '000713.jpg'], '53': ['000047.jpg', '000047.jpg', '000051.jpg', '000564.jpg', '000565.jpg', '000566.jpg', '000567.jpg', '000568.jpg', '000570.jpg', '000571.jpg', '000573.jpg', '000574.jpg', '000576.jpg', '000577.jpg', '000578.jpg', '000579.jpg', '000580.jpg', '000581.jpg', '000582.jpg', '000609.jpg', '000610.jpg', '000669.jpg', '000670.jpg', '000671.jpg', '000672.jpg', '000673.jpg', '000674.jpg', '000706.jpg', '000707.jpg', '000708.jpg', '000709.jpg'], '71': ['000078.jpg', '000078.jpg', '000079.jpg', '000080.jpg', '000081.jpg', '000082.jpg', '000083.jpg', '000084.jpg', '000085.jpg', '000087.jpg', '000090.jpg', '000180.jpg', '000181.jpg', '000182.jpg', '000183.jpg', '000184.jpg', '000186.jpg', '000188.jpg', '000189.jpg', '000191.jpg', '000192.jpg', '000194.jpg', '000195.jpg', '000196.jpg', '000197.jpg', '000200.jpg', '000201.jpg', '000202.jpg', '000203.jpg', '000204.jpg'], '51': ['000583.jpg', '000583.jpg', '000584.jpg', '000585.jpg', '000586.jpg', '000587.jpg', '000588.jpg', '000589.jpg', '000590.jpg', '000591.jpg', '000592.jpg', '000593.jpg', '000607.jpg', '000608.jpg', '000675.jpg', '000676.jpg', '000677.jpg', '000678.jpg', '000679.jpg', '000680.jpg', '000681.jpg', '000682.jpg', '000704.jpg', '000705.jpg'], '50': ['000594.jpg', '000594.jpg', '000595.jpg', '000596.jpg', '000597.jpg', '000598.jpg', '000599.jpg', '000600.jpg', '000601.jpg', '000602.jpg', '000603.jpg', '000604.jpg', '000605.jpg', '000606.jpg', '000683.jpg', '000684.jpg', '000685.jpg', '000686.jpg', '000687.jpg', '000688.jpg', '000689.jpg', '000690.jpg', '000691.jpg', '000692.jpg', '000700.jpg', '000701.jpg', '000702.jpg', '000703.jpg'], '49': ['000693.jpg', '000693.jpg', '000694.jpg', '000695.jpg', '000696.jpg', '000697.jpg', '000698.jpg', '000699.jpg']}



# {'62.', 'Gb6-', '50.', '68', 'S/', '55', '69', 'S3-', '64', 'SISE.', 'S1', '493-', '5S9O-', 'GO'}

# {'67', '60', '53', '69', 'S1', 'S/', '59', '55S', '7/1', '7', '693', '49', '50', '66', '64'}
# {'S1', '7/1', 'S/', '55S', '53', '7', '69', '59', '64', '50', '49', '67', '60', '693', '66'}
# sorted ['49', '50', '53', '55S', '59', '60', '64', '66', '67', '69', '693', '7', '7/1', 'S/', 'S1']
#        ['49', '50', '53', '55S', '59', '60', '64', '66', '67', '69', '693', '7', '7/1', 'S/', 'S1']

# {'53', '67', '7/1', '66', '7', 'S/', 'S1', '693', '60', '59', '49', '64', '69', '50', '55S'}
# {'69': 'archived_live_photos\\000207.jpg', '693': 'archived_live_photos\\000232.jpg', '66': 'archived_live_photos\\000305.jpg', '64': 'archived_live_photos\\000316.jpg', '67': 'archived_live_photos\\000541.jpg', '60': 'archived_live_photos\\000737.jpg', '59': 'archived_live_photos\\000742.jpg', 'S/': 'archived_live_photos\\000715.jpg', '55S': 'archived_live_photos\\000713.jpg', '53': 'archived_live_photos\\000709.jpg', '7/1': 'archived_live_photos\\000204.jpg', '7': 'archived_live_photos\\000199.jpg', 'S1': 'archived_live_photos\\000705.jpg', '50': 'archived_live_photos\\000703.jpg', '49': 'archived_live_photos\\000699.jpg'}

# 69 archived_live_photos\000207.jpg
# 693 archived_live_photos\000232.jpg -- 68
# 66 archived_live_photos\000305.jpg
# 64 archived_live_photos\000316.jpg
# 67 archived_live_photos\000541.jpg -- 62
# 60 archived_live_photos\000737.jpg -- 
# 59 archived_live_photos\000742.jpg
# S/ archived_live_photos\000715.jpg -- 57
# 55S archived_live_photos\000713.jpg -- 55
# 53 archived_live_photos\000709.jpg
# 7/1 archived_live_photos\000204.jpg -- 71
# 7 archived_live_photos\000199.jpg  -- 73
# S1 archived_live_photos\000705.jpg -- 51
# 50 archived_live_photos\000703.jpg
# 49 archived_live_photos\000699.jpg
# Loop through all images in the archive