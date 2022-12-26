from html2image import Html2Image
from firestore import get_allCourseInfo
from Order_and_Table import tableMaker


    #將爬蟲完的資料儲存到firestore
def map_pic_white(username):
    allCourse = get_allCourseInfo(username)
    table = tableMaker(allCourse)   #tableMaker的格式預設為html

    hti = Html2Image()
    hti.size = (900, 600)
    hti.output_path = 'static/assets'
    css = 'body {background-color: #f8f8f8; font-size: 3em; overflow:hidden;}'

    # screenshot an HTML string (css is optional)
    hti.screenshot(html_str=table, css_str=css, save_as='table.png')
    return None

#map_pic_white('b07612041')
