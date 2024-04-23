import functions_framework
import vertexai
from vertexai.language_models import TextGenerationModel
import json
import random
# import base64

vertexai.init(project="your-project-id", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40,
}

def create_and_draw_tarot_spread(spread_size=4):
    class TarotCard:
        def __init__(self, description, name, number=None, image_url=None):
            self.description = description
            self.name = name
            self.number = number
            self.image_url = image_url
            if number is None:
                self.title = name
            else:
                self.title = f"{number} of {name}"

        def __repr__(self):
            return f'{self.title} : {self.description} : {self.image_url}'

    # List of card numbers including face cards
    numbers = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Page','Knight','Queen','King']

    # Dictionary for each suit with descriptions for each number or face card
    cups_descriptions = {
        'Ace' : ("แทนถึง ความรัก การเริ่มต้น การมอบสิ่งดี ๆ ให้กับอีกฝ่ายหรืออาจจะเป็นฝ่ายได้รับสิ่งดี ๆ จากผู้อื่น","https://storage.googleapis.com/tarot_img/minor_arcana_cups_ace.png"),
        'Two' : ("แทนถึง คนรัก คู่รัก การมอบความรักให้กันและกัน ถ้าชอบใครอยู่อาจมีโอกาสสมหวัง","https://storage.googleapis.com/tarot_img/minor_arcana_cups_2.png"),
        'Three' : ("แทนถึง การเฉลิมฉลอง ปาร์ตี้กับเพื่อน ๆ มีความรักแบบเพื่อนฝูง แฮปปี้มีความสุข","https://storage.googleapis.com/tarot_img/minor_arcana_cups_3.png"),
        'Four' : ("แทนถึง การหยุดนิ่ง ความเบื่อหน่าย แม้จะมีความสุข มีสิ่งดี ๆ รายล้อม แต่กลับเบื่อหน่ายเพราะอยู่แต่ในกรอบเดิม ๆ","https://storage.googleapis.com/tarot_img/minor_arcana_cups_4.png"),
        'Five' : ("แทนถึง การสูญเสีย ความเศร้า เหมือนถ้วยที่ล้มลง ความรู้สึกสิ้นหวัง ความหวังพังทลาย","https://storage.googleapis.com/tarot_img/minor_arcana_cups_5.png"),
        'Six' : ("แทนถึง ความสงบสุข มีคนมาเยี่ยม อาจได้รับเซอร์ไพรส์จากคนอื่น มีการมาหาแบบไม่ทันตั้งตัว ได้รับของฝาก","https://storage.googleapis.com/tarot_img/minor_arcana_cups_6.png"),
        'Seven' : ("แทนถึง ความสับสน ตัวเลือกเยอะ เกิดขึ้นได้จากความรู้สึกที่มีมากมายเกินความจำเป็น หรือแม้แต่มีข้อเสนอเข้ามาเยอะมากจนตัดสินใจไม่ถูก","https://storage.googleapis.com/tarot_img/minor_arcana_cups_7.png"),
        'Eight' : ("แทนถึง การจากลา ทอดทิ้ง การเดินหนีจากสิ่งที่ทำให้ผิดหวัง หรือเรื่องนั้น ๆ ได้จบลงแล้ว ได้เวลาก้าวต่อไป","https://storage.googleapis.com/tarot_img/minor_arcana_cups_8.png"),
        'Nine' : ("แทนถึง สมหวัง ความหวังเป็นจริง สิ่งที่อยากได้กำลังจะกลายเป็นจริงแล้ว นั่งรอได้เลย","https://storage.googleapis.com/tarot_img/minor_arcana_cups_9.png"),
        'Ten' : ("แทนถึง ความสุข ครอบครัว การมีทุกอย่างพร้อม มีความสุขแบบสุด ๆ ","https://storage.googleapis.com/tarot_img/minor_arcana_cups_10.png"),
        'Page' : ("แทนถึง ความสนุก ชอบเข้าสังคม ได้พบเจอกับคนมากหน้าหลายตา หรืออาจได้รับข่าวสารบางอย่าง","https://storage.googleapis.com/tarot_img/minor_arcana_cups_page.png"),
        'Knight' : ("แทนถึง นักสู้ นักฝัน การขอร้อง ขอแต่งงาน อยากได้สิ่งใดก็ต้องออกไปฝ่าฟันเอามาให้ได้","https://storage.googleapis.com/tarot_img/minor_arcana_cups_knight.png"),
        'Queen' : ("แทนถึง สัญชาตญาณดี การพิจารณา หากต้องตัดสินใจอะไรก็ตาม ต้องคิดทบทวนอย่างรอบคอบ","https://storage.googleapis.com/tarot_img/minor_arcana_cups_queen.png"),
        'King' : ("แทนถึง ฉลาด สุขุม อดทน แม้ว่าจะต้องเจอกับเหตุการณ์ไม่มั่นคงใด ๆ ก็ต้องวางตัวหนักแน่ ใช้เหตุผลมากกว่าอารมณ์","https://storage.googleapis.com/tarot_img/minor_arcana_cups_king.png")
    }

    pentacles_descriptions = {
        'Ace' : ("แทนถึง เงินทอง ความสำเร็จ การเริ่มต้น จุดเริ่มต้นของความมั่นคงมาถึงแล้ว เตรียมรับให้ดี","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_ace.png"),
        'Two' : ("แทนถึง การตัดสินใจ การเลือกด้วยความระมัดระวัง และยังหมายถึงการหมุนเงินอีกด้วย","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_2.png"),
        'Three' : ("แทนถึง การแสดงความสามารถออกมาให้คนอื่นเห็น การมุ่งมั่นสร้างฐานะ","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_3.png"),
        'Four' : ("แทนถึง ความมั่นคง ความร่ำรวย เก็บเงินเก่งจนสร้างความมั่นคงให้ชีวิตได้ดี","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_4.png"),
        'Five' : ("แทนถึง มีปัญหาทางการเงิน การแยกจากกัน ความลำบาก ช่วยเหลือคนอื่นไม่ได้ และคนอื่นก็ไม่ได้ช่วยเหลือเช่นกัน","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_5.png"),
        'Six' : ("แทนถึง ความมีน้ำใจ การแบ่งปัน แต่ก็เป็นการแบ่งปันที่ไม่เท่าเทียม ฝ่ายใดฝ่ายหนึ่งได้มากกว่า","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_6.png"),
        'Seven' : ("แทนถึง การลงทุน รางวัลตอบแทน ได้รับผลตอบแทนของการทำงานที่ผ่านมา","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_7.png"),
        'Eight' : ("แทนถึง ขยัน ทุ่มเท ขยันทำงานสร้างเงินทองและความมั่นคงของฐานะ ต้องทำงานถึงจะได้เงิน","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_8.png"),
        'Nine' : ("แทนถึง มั่นคง มั่งคั่ง มีเงินเก็บมากมาย มีความสบายพร้อมทุกด้าน","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_9.png"),
        'Ten' : ("แทนถึง การแต่งงาน ได้รับมรดก ชีวิตดี ๆ ครอบครัวดี เงินดี ชีวิตที่พร้อมทุก ๆ ด้าน","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_10.png"),
        'Page' : ("แทนถึง ได้รับข้อเสนอ ได้รับโอกาสดี ๆ แม้จะเป็นเพียงการเริ่มต้นเล็ก ๆ ก็ตาม","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_page.png"),
        'Knight' : ("แทนถึง ความละเอียด การใส่ใจ รักอิสระ กล้าออกไปหาเส้นทางใหม่ ๆ","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_knight.png"),
        'Queen' : ("แทนถึง ใจกว้าง ความอุดมสมบูรณ์ การคิดพิจารณาอย่างละเอียดรอบคอบ","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_queen.png"),
        'King' : ("แทนถึง ประสบความสำเร็จ ร่ำรวย มีเงินทองมากมาย หวังสิ่งใดก็จะได้สิ่งนั้น ไม่ขัดสน ไม่ลำบาก","https://storage.googleapis.com/tarot_img/minor_arcana_pentacles_king.png")
    }
 
    swords_descriptions = {
        'Ace' : ("แทนถึง ความสำเร็จ จุดเริ่มต้นของสิ่งใหม่ ๆ มีคนยื่นโอกาสดี ๆ เข้ามาให้ ","https://storage.googleapis.com/tarot_img/minor_arcana_swords_ace.png"),
        'Two' : ("แทนถึง การจนมุม ขยับตัวไม่ได้ เลือกไม่ได้ว่าต้องทำอย่างไร ตัดสินใจไม่ได้","https://storage.googleapis.com/tarot_img/minor_arcana_swords_2.png"),
        'Three' : ("แทนถึง ความเสียใจ ใจสลาย ต้องเจอเรื่องผิดหวัง และยังหมายถึงเจอฝนถล่มก็ได้","https://storage.googleapis.com/tarot_img/minor_arcana_swords_3.png"),
        'Four' : ("แทนถึง การพักผ่อน นิ่งเฉย โดนกดดันจากรอบตัวจนไม่อาจตัดสินใจอะไรได้","https://storage.googleapis.com/tarot_img/minor_arcana_swords_4.png"),
        'Five' : ("แทนถึง ปัญหาต่าง ๆ ที่ถาโถมเข้ามา การไม่ลงรอยกันกับคนรอบตัว รวมไปถึงการสูญเสียบางสิ่งบางอย่าง","https://storage.googleapis.com/tarot_img/minor_arcana_swords_5.png"),
        'Six' : ("แทนถึง การละเลยปัญหา เพิกเฉยต่อปัญหา จนบานปลายและทำให้ตกอยู่ในสภาวะจำยอม หรือต้องปล่อยตัวเองไปตามน้ำ","https://storage.googleapis.com/tarot_img/minor_arcana_swords_6.png"),
        'Seven' : ("แทนถึง การขโมย ทำเรื่องผิดกฎหมายต่าง ๆ รวมถึงงานที่มีเยอะมากจนล้นมือทำไม่ทัน","https://storage.googleapis.com/tarot_img/minor_arcana_swords_7.png"),
        'Eight' : ("แทนถึง การถูกบีบบังคับจากสถานการณ์ต่าง ๆ รอบตัวจนไม่อาจขยับตัวทำอะไรได้ หรือถูกปิดหูปิดตา","https://storage.googleapis.com/tarot_img/minor_arcana_swords_8.png"),
        'Nine' : ("แทนถึง ความเครียด ความกังวล ปวดหัว คิดมาก รุนแรงถึงขั้นนอนไม่หลับ","https://storage.googleapis.com/tarot_img/minor_arcana_swords_9.png"),
        'Ten' : ("แทนถึง จุดจบ สิ้นสุด เรื่องเครียดและปวดหัวต่าง ๆ จะจบลงในไม่ช้า","https://storage.googleapis.com/tarot_img/minor_arcana_swords_10.png"),
        'Page' : ("แทนถึง การใช้สัญชาตญาณในการตัดสินใจ เชื่อมั่นในตัวเอง และต้องอดทนเอาไว้แล้วจะชนะอุปสรรคต่าง ๆ ได้","https://storage.googleapis.com/tarot_img/minor_arcana_swords_page.png"),
        'Knight' : ("แทนถึง การต่อสู้ ฝ่าฟัน ศัตรู ต้องออกแรงค่อนข้างเยอะ ต้องเหนื่อย ต้องสู้ แล้วถึงจะได้ในสิ่งที่ต้องการ","https://storage.googleapis.com/tarot_img/minor_arcana_swords_knight.png"),
        'Queen' : ("แทนถึง ความอิสระเสรี ความตรงไปตรงมา ความเด็ดเดี่ยว จัดการสิ่งใดด้วยความเด็ดขาด ไม่ลังเล","https://storage.googleapis.com/tarot_img/minor_arcana_swords_queen.png"),
        'King' : ("แทนถึง ความมุ่งมั่น ความเด็ดเดี่ยว การคิดวิเคราะห์ หากเจออุปสรรคใด ๆ ต้องใช้ทั้ง 3 อย่างเพื่อผ่านไปให้ได้ ","https://storage.googleapis.com/tarot_img/minor_arcana_swords_king.png")
    }
    
    wands_descriptions = {
        'Ace' : ("แทนถึง การได้รับข่าวสาร ได้รับโอกาส หรือได้เริ่มต้นกิจกรรมบางอย่าง","https://storage.googleapis.com/tarot_img/minor_arcana_wands_ace.png"),
        'Two' : ("แทนถึง การวางแผนการต่าง ๆ ในอนาคต ความกล้าหาญ กล้าจะก้าวออกไปยังโลกอันไม่คุ้นเคย","https://storage.googleapis.com/tarot_img/minor_arcana_wands_2.png"),
        'Three' : ("แทนถึง การเดินทางไปยังที่ที่ไม่คุ้นเคย ทำในสิ่งที่กลัว หรือการมองการณ์ไกล","https://storage.googleapis.com/tarot_img/minor_arcana_wands_3.png"),
        'Four' : ("แทนถึง การเฉลิมฉลอง การแต่งงาน หรือความสุขสมหวัง","https://storage.googleapis.com/tarot_img/minor_arcana_wands_4.png"),
        'Five' : ("แทนถึง การแข่งขันกับคนหมู่มาก อุปสรรคเยอะมาก หรือทะเลาะเบาะแว้ง ไม่ลงรอยกัน","https://storage.googleapis.com/tarot_img/minor_arcana_wands_5.png"),
        'Six' : ("แทนถึง ชัยชนะ ความสำเร็จ การเฉลิมฉลองความสำเร็จ","https://storage.googleapis.com/tarot_img/minor_arcana_wands_6.png"),
        'Seven' : ("แทนถึง ความยึดมั่น การปกป้องตัวเอง อุปสรรคหรือภาระที่ถาโถมเข้ามาพร้อม ๆ กัน","https://storage.googleapis.com/tarot_img/minor_arcana_wands_7.png"),
        'Eight' : ("แทนถึง ข่าวสาร การติดต่อสื่อสารจากทางไกล หรือมีโอกาสได้เดินทางไกล","https://storage.googleapis.com/tarot_img/minor_arcana_wands_8.png"),
        'Nine' : ("แทนถึง ความเข้มแข็งและมุ่งมั่น การตัดสินใจเลือกสิ่งสำคัญ การป้องกันตัวเอง","https://storage.googleapis.com/tarot_img/minor_arcana_wands_9.png"),
        'Ten' : ("แทนถึง ภาระหน้าที่หรือการทำงานมากเกินไปจนไม่สามารถขยับตัวไปทำสิ่งอื่น ๆ ได้","https://storage.googleapis.com/tarot_img/minor_arcana_wands_10.png"),
        'Page' : ("แทนถึง ได้รับข่าวสาร กระตือรือร้น กล้าหาญ มุ่งมั่นกับสิ่งที่เลือกแล้ว","https://storage.googleapis.com/tarot_img/minor_arcana_wands_page.png"),
        'Knight' : ("แทนถึง มั่นใจในตัวเอง ชอบเสี่ยง การลงมือทำสิ่งต่าง ๆ ด้วยความรวดเร็วว่องไว","https://storage.googleapis.com/tarot_img/minor_arcana_wands_knight.png"),
        'Queen' : ("แทนถึง การมีความคิดสร้างสรรค์ การเป็นตัวของตัวเอง","https://storage.googleapis.com/tarot_img/minor_arcana_wands_queen.png"),
        'King' : ("แทนถึง การมีอำนาจ มีไอเดียใหม่ ๆ กล้าหาญ ความมั่นคงและน่าเชื่อถือ","https://storage.googleapis.com/tarot_img/minor_arcana_wands_king.png")
    }

    minor_arcana = {
        'Cups': cups_descriptions,
        'Pentacles': pentacles_descriptions,
        'Swords': swords_descriptions,
        'Wands': wands_descriptions
    }


    # Major arcana descriptions
    major_arcana = {"The Fool": ("แทนถึงจุดเริ่มต้นใหม่ ความคิดสดใส และการก้าวข้ามด้วยความมั่นใจ","https://storage.googleapis.com/tarot_img/major_arcana_fool.png"),
                    "The Magician": ("แทนถึงการค้นพบตนเอง การทำให้เป็นจริง และพลังส่วนบุคคล","https://storage.googleapis.com/tarot_img/major_arcana_magician.png"),
                    "The High Priestess": ("แทนถึงสัญชาตญาณ การเชื่อมต่อทางจิตวิญญาณ และปัญญาภายใน", "https://storage.googleapis.com/tarot_img/major_arcana_priestess.png"),
                    "The Empress": ("แทนถึงการเลี้ยงดู ความอุดมสมบูรณ์ และความเป็นแม่", "https://storage.googleapis.com/tarot_img/major_arcana_empress.png"),
                    "The Emperor": ("แทนถึงโครงสร้าง วินัย และอำนาจ", "https://storage.googleapis.com/tarot_img/major_arcana_emperor.png"),
                    "The Hierophant": ("แทนถึงการมีความรู้ การแต่งงาน การรวมเป็นหนึ่ง", "https://storage.googleapis.com/tarot_img/major_arcana_hierophant.png"),
                    "The Lovers": ("แทนถึงความรัก ความสัมพันธ์ และการตัดสินใจ", "https://storage.googleapis.com/tarot_img/major_arcana_lovers.png"),
                    "The Chariot": ("แทนถึงพละกำลัง การควบคุม และการทำให้ความปรารถนาส่วนตัวเป็นจริง", "https://storage.googleapis.com/tarot_img/major_arcana_chariot.png"),
                    "Strength": ("แทนถึงความแข็งแกร่ง ความอดทน และพละกำลังภายใน", "https://storage.googleapis.com/tarot_img/major_arcana_strength.png"),
                    "The Hermit": ("แทนถึงการพิจารณาตนเอง ความสันโดษ และการตื่นรู้ทางจิตวิญญาณ", "https://storage.googleapis.com/tarot_img/major_arcana_hermit.png"),
                    "The Wheel of Fortune": ("แทนถึงการเปลี่ยนแปลง วงจรชีวิต และกฎแห่งกรรม", "https://storage.googleapis.com/tarot_img/major_arcana_fortune.png"),
                    "Justice": ("แทนถึงความสมดุล ความยุติธรรม และการแสวงหาความถูกต้อง", "https://storage.googleapis.com/tarot_img/major_arcana_justice.png"),
                    "The Hanged Man": ("แทนถึงการเสียสละ การปล่อยวาง และการปลดปล่อยทางอารมณ์", "https://storage.googleapis.com/tarot_img/major_arcana_hanged.png"),
                    "Death": ("แทนถึงการเปลี่ยนแปลง ความตาย และสิ้นสุดของวัฏจักร", "https://storage.googleapis.com/tarot_img/major_arcana_death.png"),
                    "Temperance": ("แทนถึงความสมดุล ความกลมกลืน และศิลปะแห่งความพอดี", "https://storage.googleapis.com/tarot_img/major_arcana_temperance.png"),
                    "The Devil": ("แทนถึงความยั่วยวน การหลอกลวงตนเอง และด้านมืดของตัวเรา", "https://storage.googleapis.com/tarot_img/major_arcana_devil.png"),
                    "The Tower": ("แทนถึงความสะเทือนขวัญ ความทุกข์ทรมาน และการสั่นคลอนโครงสร้างทางอารมณ์และจิตใจ", "https://storage.googleapis.com/tarot_img/major_arcana_tower.png"),
                    "The Star": ("แทนถึงความหวัง การชี้นำ และประกายแห่งความศักดิ์สิทธิ์ภายในตัวคนทุกคน", "https://storage.googleapis.com/tarot_img/major_arcana_star.png"),
                    "The Moon": ("แทนถึงสัญชาตญาณ อารมณ์ความรู้สึก และวัฏจักรของชีวิต", "https://storage.googleapis.com/tarot_img/major_arcana_moon.png"),
                    "The Sun": ("แทนถึงการตื่นรู้ ความรู้แจ้ง และการเติบโตส่วนบุคคล", "https://storage.googleapis.com/tarot_img/major_arcana_sun.png"),
                    "Judgement": ("แทนถึงการประเมินตนเอง การวิพากษ์วิจารณ์ภายใน และความจำเป็นต้องเปลี่ยนแปลงตนเอง", "https://storage.googleapis.com/tarot_img/major_arcana_judgement.png"),
                    "The World": ("แทนถึงความสมบูรณ์ ความสำเร็จ และตัวตนของเรามีความเชื่อมโยงอย่างลึกซึ้งกับสิ่งอื่น ๆ ทั้งหมด", "https://storage.googleapis.com/tarot_img/major_arcana_world.png")}

    # Populate the deck with major and minor arcana cards
    DECK = []
    for name, (description, image_url) in major_arcana.items():
        DECK.append(TarotCard(description, name, image_url=image_url))
    for suit, cards in minor_arcana.items():
        for number, (description, image_url) in cards.items():
            DECK.append(TarotCard(description, suit, number, image_url=image_url))

    # Draw a spread from the deck
    def draw_spread(spread):
        cards = random.sample(DECK, spread)
        spread_names = ['past', 'present', 'future', 'advice']
        return {spread_names[i]: str(cards[i]) for i in range(spread)}

    # Return the drawn cards as the result
    return draw_spread(spread_size)

@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function that interprets a tarot spread."""

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

    request_json = request.get_json(silent=True)

    if not request_json or 'question' not in request_json:
        question = "What does this tarot spread mean for my life in the upcoming week?"
    else:
        question = request_json['question']

    response_data = create_and_draw_tarot_spread()
    past = response_data['past']
    present = response_data['present']
    future = response_data['future']
    advice = response_data['advice']

    cards_format = {}
    for key, card_string in response_data.items():
        parts = card_string.split(' : ')
        card_name, description, image_url = parts[0], parts[1], parts[2]
        cards_format[key] = {
            'card_name': card_name,
            'result': description,
            'image_url': image_url
            }
    
    prompt = (f"You are a Tarot reader AI who knows about Tarot and understands the significance of different spreads in a reading. "
              f"The human has asked questions with the drawing result of Tarot, based on a 4-card spread. "
              f"The question that I want answered is:\n{question}\n"
              f"The cards I have drawn are detailed as follows:\n{json.dumps(cards_format, indent=2)}\n"
              f"it\'s a 4-card spread representing for past, present, future and advice"
              f"What does this spread mean? Answer with your own words and thoughts, and please do not repeat the answers you have mentioned before. "
              f"Reply in Thai but keep the card names in English.")

    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(prompt, **parameters)
    result_json = {**cards_format, 'conclusion': response.text}
    return (json.dumps(result_json, ensure_ascii=False), 200, headers)


