import random
import time
from pickle import dump, load

## Hayvanlar Sınıfı


class Animals:
    ## Hayvanlar
    raw_animals = {}  # hayvanların ve özelliklerinin listesi
    animals = {}  # aynı liste ama bunun üzerinde hayvanlar silinir

    raw_animal_names = []  # hayvan adlarının listesi
    animal_names = []  # aynı liste ama bunun üzerinden hayvanlar silinir

    ## Sorular
    # sorular ve sorulara yazılıcak cümleler
    questions = {"diet": "Hayvanın beslenme biçimi ne ?",
                 "size": "Hayvanın büyüklüğü ne ?",
                 "landwater": "Hayvan karada mı suda mı yaşar ?",
                 "special": "Hayvanın en bilindik özelliği nedir ?",
                 "pattern": "Hayvanın deseni var mı ?",
                 "patterntype": "Hayvanın desen tipi ne ?"}
    # sorular ve olası cevapları
    question_answers = {"diet": ("etçil", "otçul", "hepçil"),
                        "size": ("küçük", "orta", "büyük"),
                        "landwater": ("kara", "su"),
                        "pattern": ("var", "yok"),  # ikisi de olabiliyorsa None olur
                        "patterntype": ("benekli", "çizgili")  # ikisi de olabiliyorsa None olur
                        }
    # soru adları
    raw_question_names = ["diet", "size", "landwater", "special", "pattern"]
    # sorulara bağlı soru adları
    linked_questions = {"pattern": "patterntype"}
    # soruların türkçeleri
    question_names_tr = {"diet": "beslenme şekli",
                         "size": "büyüklük",
                         "landwater": "karada mı suda mı",
                         "special": "bilindik özellik",
                         "pattern": "desen",
                         "patterntype": "desen şekli"}

    question_names = raw_question_names.copy()  # sorular burdan kullanılır ve silinir
    # oyun yeniden başlatılırsa raw_guestion_names'ten yeniden yüklenir

    ## Oyun nasıl oynanır
    startlist = ["Merhabalar, Aklınızdan bir hayvan tutun.",
                 "Size sorular sorucağım ve o hayvanı bilmeye çalışacağım.",
                 "Bilmiyorum'a tıklayıp soruyu geçebilirsiniz.",
                 "Hazırsanız aklınızdan bir hayvan tutun,",
                 "ve menüye dönüp oyunu başlatın.",
                 "İYİ EĞLENCELEEERRR"]

    def __init__(self):
        pass

    ## Loading animals
    @classmethod
    def load_animals(cls):  # hayvanlar sözlüğünü dosyadan yükler
        cls.raw_animals = load(open("animals.pkl", "rb"))
        cls.animals = cls.raw_animals.copy()

    @classmethod
    def load_animal_names(cls):  # hayvanlar adları listesini dosyadan yükler
        cls.raw_animal_names = list(cls.raw_animals)
        cls.raw_animal_names.sort()
        cls.animal_names = cls.raw_animal_names.copy()

    ## Saving animals
    @classmethod
    def save_animals(cls):  # hayvanlar sözlüğünü kaydeder
        dump(cls.raw_animals, open("animals.pkl", "wb"))

    ## Reloading questions and animals
    @classmethod
    def reload_questions(cls):  # soruları tekrar yükler
        cls.question_names = cls.raw_question_names.copy()

    @classmethod
    def reload_animals(cls):  # hayvanları tekrar yükler
        cls.load_animals()
        cls.load_animal_names()

    @classmethod
    def choose_question(cls):  # rastgele soru seçer
        return random.choice(cls.question_names)

    @classmethod
    def is_any_animal(cls):  # listede hayvan kalmadıysa False döndürür
        return False if not len(cls.animal_names) else True

    @classmethod
    def is_any_question(cls):  # sorular biterse False döndürür
        return False if not len(cls.question_names) else True

    ## Checking answers
    @classmethod
    def answer_special(cls, answer):  # special sorusu ve verilen cevap test edilir
        i = 0
        dont_know = True

        for animal in cls.animal_names:
            if cls.animals[animal]["special"] in answer:
                dont_know = False
                while i < len(cls.animal_names):
                    animal_now = cls.animal_names[i]
                    if cls.animals[animal_now]["special"] not in answer:
                        del cls.animals[animal_now]
                        cls.animal_names.remove(animal_now)
                    else:
                        i += 1
                break

        return dont_know

    @classmethod
    def answer_normal(cls, answer, question):  # diğer sorular ve verilen cevap test edilir
        j = 0

        while j < len(cls.animal_names):
            animal = cls.animal_names[j]
            if cls.animals[animal][question] not in [answer, "None"]:
                del cls.animals[animal]
                cls.animal_names.remove(animal)
            else:
                j += 1

    @classmethod
    def guess(cls):  # listeden rastgele bir hayvan tahmin eder
        return random.choice(cls.animal_names)

    ## Add, del animals
    @classmethod
    def del_animal(cls, animal):
        del cls.raw_animals[animal]

    @classmethod
    def add_animal(cls, name, diet, size, landwater, special, pattern, patterntype):
        if pattern == "":
            pattern = "None"
        if patterntype == "":
            patterntype = "None"
        cls.raw_animals[name] = {"diet": diet,
                                 "size": size,
                                 "landwater": landwater,
                                 "special": special,
                                 "pattern": pattern,
                                 "patterntype": patterntype}
        cls.save_animals()
        cls.reload_animals()

    ## Change features and save
    @classmethod
    def change_feature(cls, animal, feature, new_feature):
        if new_feature == "":
            cls.raw_animals[animal][feature] = "None"
        else:
            cls.raw_animals[animal][feature] = new_feature
        cls.save_animals()
        cls.load_animals()
        cls.load_animal_names()
