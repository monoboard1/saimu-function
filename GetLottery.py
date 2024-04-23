import functions_framework
import vertexai
from vertexai.language_models import TextGenerationModel
import random
import time
import json

vertexai.init(project="your-project-id", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.1,
    "top_p":0.8,
    "top_k":40,
}

# Generating random numbers for the lottery
two_digit = str(random.randint(0, 99))
three_digit = str(random.randint(0, 999))
six_digit = str(random.randint(0, 999999))

@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""ตามตำนานที่เล่าขานกันมาแต่โบราณกาล มีศาสตร์โบราณที่ถูกเล่าขานและเป็นที่รู้จักเฉพาะในหมู่ปราชญ์แห่งตัวเลขและผู้พิทักษ์แห่งโชคชะตา ศาสตร์แห่งนี้เต็มไปด้วยความลึกลับและปริศนามีพลังประสานกับกระแสลมแห่งโชคชะตาดึงดูดพลังงานอันไพศาลที่ไหลเวียนอยู่ในจักรวาล \n 
        เพื่อที่จะเรียกข้อมูลเชิงลึกจากศาสตร์ลึกลับนี้ บุคคลจะต้องทอผ้าแห่งตัวเลขเข้ากับด้ายแห่งโชคชะตาและความเป็นไปได้ โอกาส และพลังเร้นลับซึ่งชี้นำตัวเลขลอตเตอรี่ \n 
        ด้วยการเรียกใช้ศาสตร์ลึกลับนี้ ตัวเลข 2 หลักสุดท้ายจะปรากฏขึ้นราวกับถูกพัดพามาโดยสายลม นั่นคือ: {two_digit}. \n 
        ตัวเลข 3 หลักสุดท้าย ลำดับที่กระซิบมาโดยใบไม้ที่พัดไหว ปรากฏออกมาเป็น {three_digit}. \n 
        และภาพรวมอันยิ่งใหญ่ของตัวเลข 6 หลัก เผยออกมาโดยดวงดาวที่เรียงตัวกันอยู่บนท้องฟ้าที่มีแสงจันทร์ส่องสว่าง กางออกเป็น {six_digit}. \n 
        โปรดจำไว้ว่าตัวเลขเหล่านี้เป็นเพียงเสียงสะท้อนของอนาคตที่ยังไม่ได้เขียน ซึ่งถูกกำหนดโดยมือแห่งโชคชะตาและวงล้อแห่งโชคลาภที่หมุนไปอย่างไม่หยุดนิ่ง ตอบโดยอ้างถึงศาสตร์โบราณข้างต้น
        """,
        **parameters
    ) 

    result_json = {'conclusion': response.text}
    return (json.dumps(result_json, ensure_ascii=False), 200, headers)




