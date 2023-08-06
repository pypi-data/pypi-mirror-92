import pprint
from findit import FindIt

fi = FindIt(engine=["template", "feature"], need_log=True)
fi.load_template("wechat_logo", pic_path="../qq.png")
# fi.load_template('app_store_logo', pic_path='pics/app_store_logo.png')

result = fi.find(target_pic_name="screen", target_pic_path="../b.png")

pprint.pprint(result)

import cv2

p = cv2.imread("../b.png")
point = tuple(map(int, result["data"]["wechat_logo"]["TemplateEngine"]["target_point"]))
p1 = cv2.circle(p, point, 10, (0, 255, 0))
cv2.imshow("", p1)
cv2.waitKey(0)
