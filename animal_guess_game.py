from animals import Animals as An
import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import pyautogui
from hashlib import sha256


# Ana Oyun
class Game(tk.Tk):

    ## Monitor size, middle point of monitor
    monitor = pyautogui.size()  # returns monitor resolution -> (width, height)
    monitor_width, monitor_height = monitor[0], monitor[1]
    width, height = 600, 700
    center_width, center_height = (monitor_width - width) // 2, (monitor_height - height) // 2
    ## Admin mod and password
    admin_access = False  # this turns True when password is entered
    password_hash = "d2bffb8c94703676567ac7cdb38b1a7a2ce9283d45aaab07201635250de67de0"
    ## Showing animals
    show_animals_list = []  # this list used to show animals in show animals function
    animal_no = 0  # number of first animal in show animal list
    animal_num_to_show = 3  # the count of animals to show in page
    ## Adding features
    can_add = True
    feature_to_add = ""
    animal_number = 0
    ## Questions
    last_question = ""
    last_answer = ""

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Hayvan Tahmin Oyunu")  # Animal Guess Game
        self.iconbitmap("pati.ico")  # oyunun ikonu pati
        self.protocol("WM_DELETE_WINDOW", self.exit_or_not)  # çarpıya basıldığında çalışır
        self.geometry("{}x{}+{}+{}".format(self.width, self.height,
                                           self.center_width, self.center_height))

        An.load_animals()
        An.load_animal_names()

        self._frame = None
        self.switch_frame(StartPage)

    ## switching pages(frames)
    def switch_frame(self, frame_class):  # sayfa değiştir
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    ## Checking passwords
    @staticmethod
    def password_to_hash(password):  # girilen şifreyi hashe çevirir
        pw_bytestring = password.encode()
        return sha256(pw_bytestring).hexdigest()

    def password_check_or_not(self):
        if self.admin_access:
            self.switch_frame(SpecialFuncsPage)
        else:
            self.switch_frame(PasswordCheckPage)

    def password_check(self, entered_password):  # girilen parola test edilir
        entered_password_hash = self.password_to_hash(entered_password)
        if entered_password_hash == self.password_hash:
            self.admin_access = True
            self.switch_frame(SpecialFuncsPage)
        else:
            messagebox.showerror("Hata !", "Yanlış Parola Girildi !")
            self.switch_frame(StartPage)

    ## Add animals
    def add_animal(self, name, diet, size, landwater, special, pattern, patterntype):
        self.can_add = True
        if not name:
            messagebox.showwarning("Hata !", "Hayvanın ismini yazın.")
        if diet not in An.question_answers["diet"]:
            messagebox.showwarning("Hata !", "Beslenme şeklini menüsünden seçin.")
        if size not in An.question_answers["size"]:
            messagebox.showwarning("Hata !", "Büyüklüğünü menüsünden seçin.")
        if landwater not in An.question_answers["landwater"]:
            messagebox.showwarning("Hata !", "Karada mı suda mı yaşadığını menüsünden seçin.")
        else:
            if not special:
                special = "None"
            if name in An.raw_animal_names:
                response = messagebox.askyesno("Dikkat !",
                                               "{} hayvanı zaten var. Onun yerine eklemek ister misin?".format(name))
                self.can_add = response
            if self.can_add:
                An.add_animal(name, diet, size, landwater, special, pattern, patterntype)
                messagebox.showinfo("", "{} hayvanı eklendi.".format(name))
                self.switch_frame(SpecialFuncsPage)

    ## Deleting animals
    def check_to_del(self, animal):
        if animal == "animal":
            messagebox.showwarning("Hata !", "Bir Hayvan Seçin.")
        else:
            response = messagebox.askyesno("Dikkat!", "{} hayvanını silmek istediğine emin misin ?".format(animal))
            if response:
                An.del_animal(animal)
                An.save_animals()
                An.reload_animals()
                messagebox.showinfo("", "{} hayvanı silindi.".format(animal))
                self.switch_frame(DelAnimalPage)

    ## Showing animals, features
    def show_animals(self, first_animal_no):  # girilen sayıyla başlayan birkaç hayvanlı bir
        self.show_animals_list = []                # liste oluşturulur
        self.animal_no = first_animal_no
        for i in range(first_animal_no, first_animal_no + self.animal_num_to_show):
            try:
                self.show_animals_list.append(An.raw_animal_names[i])
            except:
                pass
        self.switch_frame(ShowAnimalsPage)

    @staticmethod
    def show_feature(animal, feature):  # hayvanın bir özelliğini gösterme
        if animal == "animal":  # hayvan seçilmediyse
            messagebox.showwarning("Hata !", "Bir Hayvan Seçin.")
        elif feature == "":  # özellik seçilmediyse
            messagebox.showwarning("Hata !", "Bir Özellik Seçin.")
        else:
            messagebox.showinfo("Özellik",
                                "{} hayvanının {} özelliği: {}".format(animal, An.question_names_tr[feature],
                                                                       An.raw_animals[animal][feature]))

    ## Adding features
    def add_feature(self, feature):
        # if feature in An.raw_question_names or feature in An.question_names_tr.values():
        #     messagebox.showinfo("Hata !", "Bu özellik zaten var.")
        # else:
        self.feature_to_add = feature
        self.switch_frame(AddFeatureToAnimalsPage)

    def feature_to_animals(self, feature):
        animal = An.raw_animal_names[self.animal_number]
        if feature == "":
            An.raw_animals[animal][self.feature_to_add] = "None"
        else:
            An.raw_animals[animal][self.feature_to_add] = feature
        self.animal_number += 1

        if self.animal_number == len(An.raw_animal_names):
            An.save_animals()
            messagebox.showinfo("Tamamlandı", "Tüm hayvanlara özellik eklendi.")
            self.switch_frame(SpecialFuncsPage)
        else:
            self.switch_frame(AddFeatureToAnimalsPage)

    def discard_features(self):
        An.reload_animals()
        self.switch_frame(SpecialFuncsPage)

    ## Changing features
    def change_or_not(self, animal, feature, new_feature):
        if animal == "animal":  # hayvan seçilmediyse,
            messagebox.showwarning("Hata !", "Bir Hayvan Seçin.")
        elif feature == "feature":  # özellik seçilmediyse,
            messagebox.showwarning("Hata !", "Bir Özellik Seçin.")
        # girilen özellik girilebilicek özelliklerde yoksa hata verir
        elif (feature not in ["special", "pattern", "patterntype"]) and (new_feature not in An.question_answers[feature]):
            messagebox.showwarning("Hata !",
                                   "Şu özelliklerden birini yazın:{}.".format(An.question_answers[feature]))
        else:
            # hayvanın özelliğini değiştir ve kaydet
            An.change_feature(animal, feature, new_feature)
            self.switch_frame(SpecialFuncsPage)

    ## Control answers
    def answer_special(self, answer):  # bilindik özellik cevabı test ediliyor
        dont_know = An.answer_special(answer)
        An.question_names.remove("special")

        if dont_know:
            self.switch_frame(NoSpecialPage)
        else:
            self.switch_frame(AnimalGuessPage)

    def answer_normal(self, answer, question):  # diğer soruların cevabı test ediliyor
        self.last_question = question
        self.last_answer = answer

        if not An.is_any_animal:
            self.switch_frame(AnimalGuessPage)

        An.answer_normal(answer, question)
        if question in An.question_names:
            An.question_names.remove(question)

        self.switch_frame(AnimalGuessPage)

    ## Control guesses
    def wrong_guess(self, animal):
        del An.animals[animal]
        An.animal_names.remove(animal)
        self.is_any_animal()

    def is_any_animal(self):
        if not An.is_any_animal():
            self.switch_frame(AnimalGuessPage)
        elif not An.is_any_question():
            self.switch_frame(NoQuestionGuessPage)
        else:
            self.switch_frame(QuestionPage)

    ## Restart, Main Menu, Exit
    def restart(self):  # oyunu yeniden başlat
        An.load_animals()
        An.load_animal_names()
        An.reload_questions()
        self.last_question = ""
        self.last_answer = ""
        self.switch_frame(QuestionPage)

    def mainmenu(self):  # ana menüye dön
        An.load_animals()
        An.load_animal_names()
        An.reload_questions()
        self.last_question = ""
        self.last_answer = ""
        self.switch_frame(StartPage)

    def exit_or_not(self):  # çarpıya basıldığında çıkmak istiyor musun diye sorar
        self.switch_frame(ExitPage)

    @staticmethod
    def exit():  # Oyundan çık
        try:
            sys.exit(0)
        except:
            os._exit(0)


# Oyunun ana menüsü
class StartPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.special_funcs_btn = tk.Button(self, text="HAYVAN TAHMİN OYUNUNA HOŞGELDİNİZ", height=1,
                                           command=master.password_check_or_not, relief=tk.FLAT, bd=0)  # şifre kontrol
        self.start_btn = tk.Button(self, text="Başla", height=5, width=15,
                                   command=lambda: master.switch_frame(QuestionPage))  # Start
        self.how_to_btn = tk.Button(self, text="Nasıl Oynanır", height=5, width=15,
                                    command=lambda: master.switch_frame(HowToPage))  # How to Play
        self.exit_btn = tk.Button(self, text="Çık", height=5, width=15,
                                  command=lambda: master.switch_frame(ExitPage))  # Exit

        self.special_funcs_btn.pack(padx=20, pady=20)
        self.start_btn.pack(padx=20, pady=20)
        self.how_to_btn.pack(padx=20, pady=20)
        self.exit_btn.pack(padx=20, pady=20)
        self.start_btn.focus()


# Soru sorulan sayfa
class QuestionPage(tk.LabelFrame):
    # Yazarken yanlış gözüken harfler ve karşılıkları
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        if (master.last_question in An.linked_questions) and (master.last_answer == An.question_answers[master.last_question][0]):
            self.question = An.linked_questions[master.last_question]
        else:
            self.question = An.choose_question()

        self.restart_frame = tk.Frame(self)
        self.restart_frame.pack(fill="x")

        self.rstrt_btn = tk.Button(self.restart_frame, text="Baştan Başla", height=3, width=12,
                                   command=lambda: master.restart())
        self.mainmenu_btn = tk.Button(self.restart_frame, text="Ana Menü", height=3, width=12,
                                      command=lambda: master.mainmenu())
        self.rstrt_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.mainmenu_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.question_frame = tk.Frame(self)
        self.question_frame.pack(fill="x", expand=True)

        self.question_lbl = tk.Label(self.question_frame, text=An.questions[self.question],
                                     pady=30)
        self.question_lbl.pack(side=tk.BOTTOM)

        if self.question == "special":  # seçilen soru special sorusuysa
            self.var = tk.StringVar()
            self.var.trace_variable("w", self.validate)  # anında düzeltme fonksiyonu çalışır

            self.answer_special_frame = tk.Frame(self, width=400)
            self.answer_special_frame.pack(expand=True)

            self.answer_special_lbl = tk.Label(self.answer_special_frame, text="Cevabınızı girin: ")
            self.answer_special_lbl.grid(row=0, column=0, padx=10)

            self.answer_special_entry = tk.Entry(self.answer_special_frame, textvariable=self.var, width=20)
            self.answer_special_entry.grid(row=0, column=1, padx=10)
            self.answer_special_entry.focus()
            # Enter
            self.answer_special_btn = tk.Button(self.answer_special_frame, text="Gir", padx=15, pady=5,
                                                command=lambda: master.answer_special(self.answer_special_entry.get()))
            self.answer_special_btn.grid(row=0, column=2, padx=10)

        else:  # diğer sorularda
            self.answers_frame = tk.Frame(self, width=400)
            self.answers_frame.pack(expand=True)

            self.answer_no = 0
            for answer in An.question_answers[self.question]:
                tk.Button(self.answers_frame, text=answer.title(), padx=10, pady=10,
                          command=lambda answer=answer: master.answer_normal(answer, self.question)).grid(row=0,
                                                                                                          padx=10,
                                                                                                          column=self.answer_no)
                self.answer_no += 1

        self.dont_know_frame = tk.Frame(self)
        self.dont_know_frame.pack(fill="both", expand=True)

        self.dont_know_btn = tk.Button(self.dont_know_frame, text="Bilmiyorum", padx=10, pady=10,
                                       command=lambda: master.switch_frame(DontKnowPage))
        self.dont_know_btn.pack(pady=10)

    def validate(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.var.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.var.set("".join(text))


# Hayvan tahmin edilen sayfa
class AnimalGuessPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.restart_frame = tk.Frame(self)
        self.restart_frame.pack(fill="x")

        self.rstrt_btn = tk.Button(self.restart_frame, text="Baştan Başla", height=3, width=12,
                                   command=lambda: master.restart())
        self.mainmenu_btn = tk.Button(self.restart_frame, text="Ana Menü", height=3, width=12,
                                      command=lambda: master.mainmenu())
        self.rstrt_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.mainmenu_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        try:  # if there are animals, this will guess an animal
            self.guess = An.guess()

            self.guess_frame = tk.Frame(self)
            self.guess_frame.pack(fill="both", expand=True)

            self.guess_label = tk.Label(self.guess_frame, text="O zaman bence tuttuğun hayvaaannnn...")

            self.guess_label3 = tk.Label(self.guess_frame, text="Doğru mu Yanlış mı ?")

            self.guess_label2 = tk.Label(self.guess_frame, text="Bir {}".format(self.guess))

            self.guess_answer_frame = tk.Frame(self)
            self.guess_answer_frame.pack(fill="y", expand=True)

            self.guess_yes_btn = tk.Button(self.guess_answer_frame, text="Doğru", padx=10,
                                           command=lambda: master.switch_frame(FinishPage))
            self.guess_no_btn = tk.Button(self.guess_answer_frame, text="Yanlış", padx=10,
                                          command=lambda: master.wrong_guess(self.guess))

            self.guess_label.pack(pady=40, side=tk.TOP)
            self.after(1000, self.guess_is)
            self.after(1500, self.correct_or_not)

        except:  # to NoAnimalPage
            self.finish_frame = tk.Frame(self)
            self.finish_frame.pack(fill="both", expand=True)

            self.finish_lbl = tk.Label(self.finish_frame,
                                       text="Üzgünüm, böyle bir hayvan bulamadım.\n\nŞimdi napalıım ?")
            self.finish_lbl.pack(side=tk.BOTTOM)

            self.finish_btn_frame = tk.Frame(self)
            self.finish_btn_frame.pack(fill="y", expand=True)

            self.restart_btn = tk.Button(self.finish_btn_frame, text="Yeniden Oynayalım", padx=10, pady=10,
                                         command=lambda: master.restart())
            self.exit_btn = tk.Button(self.finish_btn_frame, text="Çık", padx=10, pady=10,
                                      command=lambda: master.switch_frame(ExitPage))
            self.restart_btn.pack(side=tk.LEFT, padx=10)
            self.exit_btn.pack(side=tk.LEFT, padx=10)
            self.restart_btn.focus()

    def guess_is(self):
        self.guess_label2.pack(pady=20, side=tk.TOP)

    def correct_or_not(self):
        self.guess_label3.pack(pady=20, side=tk.TOP)
        self.guess_yes_btn.pack(side=tk.LEFT, padx=10)
        self.guess_no_btn.pack(side=tk.LEFT, padx=10)


# Hayvan var ama soru yoksa gidilen sayfa
class NoQuestionGuessPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.guess_or_not_frame = tk.Frame(self)
        self.guess_or_not_frame.pack(fill="both", expand=True)

        self.guess_or_not_label = tk.Label(self.guess_or_not_frame,
                                           text="Sorum kalmadı, tahmin edim mi ?")
        self.guess_or_not_label.pack(side=tk.BOTTOM, pady=20)

        self.guess_btn_frame = tk.Frame(self)
        self.guess_btn_frame.pack(fill="y", expand=True)

        self.guess_btn = tk.Button(self.guess_btn_frame, text="Tahmin Et", padx=10, pady=10,
                                   command=lambda: master.switch_frame(AnimalGuessPage))
        self.restart_btn = tk.Button(self.guess_btn_frame, text="Yeniden Oynayalım", padx=10, pady=10,
                                     command=lambda: master.restart())
        self.exit_btn = tk.Button(self.guess_btn_frame, text="Çık", padx=10, pady=10,
                                  command=lambda: master.switch_frame(ExitPage))

        self.guess_btn.pack(side=tk.LEFT, padx=10)
        self.restart_btn.pack(side=tk.LEFT, padx=10)
        self.exit_btn.pack(side=tk.LEFT, padx=10)
        self.guess_btn.focus()


# Hiç hayvan kalmadıysa gidilen sayfa
class NoAnimalPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.finish_frame = tk.Frame(self)
        self.finish_frame.pack(fill="both", expand=True)

        self.finish_lbl = tk.Label(self.finish_frame, text="Üzgünüm, böyle bir hayvan bulamadım.\n\nŞimdi napalıım ?")
        self.finish_lbl.pack(side=tk.BOTTOM)

        self.finish_btn_frame = tk.Frame(self)
        self.finish_btn_frame.pack(fill="y", expand=True)

        self.restart_btn = tk.Button(self.finish_btn_frame, text="Yeniden Oynayalım", padx=10, pady=10,
                                     command=lambda: master.restart())
        self.exit_btn = tk.Button(self.finish_btn_frame, text="Çık", padx=10, pady=10,
                                  command=lambda: master.switch_frame(ExitPage))
        self.restart_btn.pack(side=tk.LEFT, padx=10)
        self.exit_btn.pack(side=tk.LEFT, padx=10)
        self.restart_btn.focus()


# Bilindik özelliğe girilen cevap bulunamazsa gidilen sayfa
class NoSpecialPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.sorry_frame = tk.Frame(self)
        self.sorry_frame.pack(fill="both", expand=True)

        if not An.is_any_question():
            self.sorry_lbl = tk.Label(self.sorry_frame,
                                      text="Üzgünüm, bu özellikte bir hayvan bulamadım ve başka sorum kalmadı.\n\nŞimdi napalım ?")
            self.sorry_lbl.pack(pady=100)

        else:
            self.sorry_lbl = tk.Label(self.sorry_frame,
                                      text="Üzgünüm, bu özellikte bir hayvan bulamadım.\n\nBaşka soruya geçelim bakalıımm...")
            self.sorry_lbl.pack(pady=100)

        self.pass_btn_frame = tk.Frame(self)
        self.pass_btn_frame.pack(fill="y", expand=True)

        if not An.is_any_question():
            self.guess_btn = tk.Button(self.pass_btn_frame, text="Tahmin et", padx=10, pady=10,
                                       command=lambda: master.switch_frame(AnimalGuessPage))
            self.restart_btn = tk.Button(self.pass_btn_frame, text="Yeniden Oynayalım", padx=10, pady=10,
                                         command=lambda: master.restart())
            self.exit_btn = tk.Button(self.pass_btn_frame, text="Çık", padx=10, pady=10,
                                      command=lambda: master.switch_frame(ExitPage))
            self.guess_btn.pack(side=tk.LEFT, padx=10)
            self.restart_btn.pack(side=tk.LEFT, padx=10)
            self.exit_btn.pack(side=tk.LEFT, padx=10)
            self.guess_btn.focus()
        else:
            self.pass_btn = tk.Button(self.pass_btn_frame, text="Yeni soruya geç", padx=10, pady=10,
                                      command=lambda: master.switch_frame(QuestionPage))
            self.pass_btn.pack()
            self.pass_btn.focus()


# Soruya bilmiyorum cevabı verilirse gidilen sayfa
class DontKnowPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        # son soru ve cevap sıfırlanır
        master.last_question = ""
        master.last_answer = ""

        self.restart_frame = tk.Frame(self)
        self.restart_frame.pack(fill="x")

        self.rstrt_btn = tk.Button(self.restart_frame, text="Baştan Başla", height=3, width=12,
                                   command=lambda: master.restart())
        self.mainmenu_btn = tk.Button(self.restart_frame, text="Ana Menü", height=3, width=12,
                                      command=lambda: master.mainmenu())
        self.rstrt_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.mainmenu_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.dont_know_frame = tk.Frame(self)
        self.dont_know_frame.pack(fill="both", expand=True)

        self.dont_know_lbl = tk.Label(self.dont_know_frame,
                                      text="Hmmm, tamam o zamaann.\n\nBaşka soruya geçelim bakalıımm...")
        self.dont_know_lbl.pack(pady=100)

        self.pass_btn_frame = tk.Frame(self)
        self.pass_btn_frame.pack(fill="y", expand=True)

        self.pass_btn = tk.Button(self.pass_btn_frame, text="Yeni soruya geç", padx=10, pady=10,
                                  command=lambda: master.switch_frame(QuestionPage))
        self.pass_btn.pack()
        self.pass_btn.focus()


# Hayvan doğru tahmin edilirse gidilen sayfa
class FinishPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.finish_frame = tk.Frame(self)
        self.finish_frame.pack(fill="both", expand=True)

        self.finish_lbl = tk.Label(self.finish_frame, text="Güzel bir hayvan tutmuşsuunn.\n\nŞimdi napalıım ?")
        self.finish_lbl.pack(side=tk.BOTTOM)

        self.finish_btn_frame = tk.Frame(self)
        self.finish_btn_frame.pack(fill="y", expand=True)

        self.restart_btn = tk.Button(self.finish_btn_frame, text="Yeniden Oynayalım", padx=10, pady=10,
                                     command=lambda: master.restart())
        self.exit_btn = tk.Button(self.finish_btn_frame, text="Çık", padx=10, pady=10,
                                  command=lambda: master.switch_frame(ExitPage))
        self.restart_btn.pack(side=tk.LEFT, padx=10)
        self.exit_btn.pack(side=tk.LEFT, padx=10)
        self.restart_btn.focus()


# Şifreyi girdiğimiz sayfa
class PasswordCheckPage(tk.LabelFrame):
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.var = tk.StringVar()
        self.var.trace_variable("w", self.validate)  # anında düzeltme fonksiyonu çalışır
        self.password = ""

        self.password_frame = tk.Frame(self)
        self.password_frame.pack(fill="both", expand=True)

        self.password_lbl = tk.Label(self.password_frame,
                                     text="Özel fonksiyonlara erişmek için şifreyi girmeniz gerek.")
        self.password_lbl.pack(side=tk.BOTTOM, pady=20)

        self.password_check_frame = tk.Frame(self)
        self.password_check_frame.pack(fill="y", expand=True)

        self.password_check_lbl = tk.Label(self.password_check_frame,
                                           text="Şifreyi Girin: ")
        self.password_check_entry = tk.Entry(self.password_check_frame,
                                             textvariable=self.var, width=20)
        self.password_check_btn = tk.Button(self.password_check_frame, text="Gir", padx=10, pady=10,
                                            command=lambda: master.password_check(self.password))
        self.back_btn = tk.Button(self.password_check_frame, text="Geri", padx=10, pady=10,
                                  command=lambda: master.switch_frame(StartPage))
        self.password_check_lbl.pack(side=tk.LEFT, padx=10)
        self.password_check_entry.pack(side=tk.LEFT, padx=10)
        self.password_check_btn.pack(side=tk.LEFT, padx=10)
        self.back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.password_check_entry.focus()

    def validate(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.var.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        try:
            self.password += text[-1]
        except:
            self.password = ""
        self.var.set("*" * len(text))


# Özel fonksiyonların olduğu sayfa (hayvan ekle, hayvanları göster vb.)
class SpecialFuncsPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        master.show_animals_list = []  # reset list which has several animals to show

        self.show_animals_btn = tk.Button(self, text="Hayvanları Göster", height=3, width=15,
                                          command=lambda: master.show_animals(0))
        self.add_animal_btn = tk.Button(self, text="Hayvan Ekle", height=3, width=15,
                                        command=lambda: master.switch_frame(AddAnimalPage))
        self.del_animal_btn = tk.Button(self, text="Hayvan sil", height=3, width=15,
                                        command=lambda: master.switch_frame(DelAnimalPage))
        self.add_feature_btn = tk.Button(self, text="Özellik Ekle", height=3, width=15,
                                         command=lambda: master.switch_frame(AddFeaturePage))
        self.change_feature_btn = tk.Button(self, text="Özellik Değiştir", height=3, width=15,
                                            command=lambda: master.switch_frame(ChangeFeaturePage))
        self.main_menu_btn = tk.Button(self, text="Ana Menü", height=3, width=15,
                                       command=lambda: master.switch_frame(StartPage))
        self.show_animals_btn.pack(pady=30)
        self.add_animal_btn.pack(pady=0)
        self.del_animal_btn.pack(pady=30)
        self.add_feature_btn.pack(pady=0)
        self.change_feature_btn.pack(pady=30)
        self.main_menu_btn.pack(pady=0)


# birkaç hayvanın gösterildiği sayfa
class ShowAnimalsPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)
        self.row = 0

        for animal in master.show_animals_list:
            self.animals_frame = tk.Frame(self)
            self.animals_frame.pack(fill="both", expand=True)

            tk.Label(self.animals_frame, text=animal).pack(side=tk.TOP, pady=5)
            self.row += 1
            for feature in An.raw_animals[animal]:
                tk.Label(self.animals_frame,
                         text="{}: {}".format(An.question_names_tr[feature],
                                              An.raw_animals[animal][feature])).pack(side=tk.TOP,
                                                                                     padx=5)
                self.row += 1

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(fill="y", expand=True)

        self.to_functions_btn = tk.Button(self.buttons_frame, text="Fonksiyonlara", height=3, width=15,
                                          command=lambda: master.switch_frame(SpecialFuncsPage))
        self.back_btn = tk.Button(self.buttons_frame, text="Geri", height=3, width=15,
                                  command=lambda: master.show_animals(master.animal_no - master.animal_num_to_show))
        self.forward_btn = tk.Button(self.buttons_frame, text="İleri", height=3, width=15,
                                     command=lambda: master.show_animals(master.animal_no + master.animal_num_to_show))

        if An.raw_animal_names[0] in master.show_animals_list:     # ilk sayfadaysa geri butonu,
            self.back_btn["state"] = "disabled"                    #
        elif An.raw_animal_names[-1] in master.show_animals_list:  # son sayfadaysa ileri butonu
            self.forward_btn["state"] = "disabled"                 # pasif hale getirilir

        self.to_functions_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.forward_btn.pack(side=tk.LEFT, padx=10, pady=10)


# Hayvan ekleme sayfası
class AddAnimalPage(tk.LabelFrame):
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.animal_name_frame = tk.Frame(self)
        self.animal_name_frame.pack(fill="y", expand=True)

        self.animal_name = tk.StringVar()
        self.animal_name.trace_variable("w", self.validate_name)

        self.animal_name_lbl = tk.Label(self.animal_name_frame, text="Hayvanın Adı: ")
        self.animal_name_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_name_entry = tk.Entry(self.animal_name_frame, textvariable=self.animal_name,
                                          width=15)
        self.animal_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_diet_frame = tk.Frame(self)
        self.animal_diet_frame.pack(fill="y", expand=True)

        self.diet = tk.StringVar()
        self.diet.set("")

        self.animal_diet_lbl = tk.Label(self.animal_diet_frame, text="Beslenme Şekli: ")
        self.animal_diet_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_diet_dropdown = ttk.Combobox(self.animal_diet_frame, textvariable=self.diet,
                                                 values=An.question_answers["diet"])
        self.animal_diet_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_size_frame = tk.Frame(self)
        self.animal_size_frame.pack(fill="y", expand=True)

        self.size = tk.StringVar()
        self.size.set("")

        self.animal_size_lbl = tk.Label(self.animal_size_frame, text="Büyüklük: ")
        self.animal_size_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_size_dropdown = ttk.Combobox(self.animal_size_frame, textvariable=self.size,
                                                 values=An.question_answers["size"])
        self.animal_size_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_landwater_frame = tk.Frame(self)
        self.animal_landwater_frame.pack(fill="y", expand=True)

        self.landwater = tk.StringVar()
        self.landwater.set("")

        self.animal_landwater_lbl = tk.Label(self.animal_landwater_frame, text="Karada mı suda mı: ")
        self.animal_landwater_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_landwater_dropdown = ttk.Combobox(self.animal_landwater_frame, textvariable=self.landwater,
                                                      values=An.question_answers["landwater"])
        self.animal_landwater_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_special_frame = tk.Frame(self)
        self.animal_special_frame.pack(fill="y", expand=True)

        self.special = tk.StringVar()
        self.special.trace_variable("w", self.validate_special)

        self.animal_special_lbl = tk.Label(self.animal_special_frame, text="Bilindik Özelliği: ")
        self.animal_special_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_special_entry = tk.Entry(self.animal_special_frame, textvariable=self.special,
                                             width=15)
        self.animal_special_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_pattern_frame = tk.Frame(self)
        self.animal_pattern_frame.pack(fill="y", expand=True)

        self.pattern = tk.StringVar()
        self.pattern.set("")

        self.animal_pattern_lbl = tk.Label(self.animal_pattern_frame, text="Deseni var mı: ")
        self.animal_pattern_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_pattern_dropdown = ttk.Combobox(self.animal_pattern_frame, textvariable=self.pattern,
                                                    values=An.question_answers["pattern"])
        self.animal_pattern_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_patterntype_frame = tk.Frame(self)
        self.animal_patterntype_frame.pack(fill="y", expand=True)

        self.patterntype = tk.StringVar()
        self.patterntype.set("")

        self.animal_patterntype_lbl = tk.Label(self.animal_patterntype_frame, text="Deseninin şekli ne: ")
        self.animal_patterntype_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.animal_patterntype_dropdown = ttk.Combobox(self.animal_patterntype_frame, textvariable=self.patterntype,
                                                        values=An.question_answers["patterntype"])
        self.animal_patterntype_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="y", expand=True)

        self.back_btn = tk.Button(self.button_frame, text="Geri", height=3, width=10,
                                  command=lambda: master.switch_frame(SpecialFuncsPage))
        self.add_btn = tk.Button(self.button_frame, text="Ekle", height=3, width=10,
                                 command=lambda: master.add_animal(self.animal_name_entry.get(),
                                                                   self.animal_diet_dropdown.get(),
                                                                   self.animal_size_dropdown.get(),
                                                                   self.animal_landwater_dropdown.get(),
                                                                   self.animal_special_entry.get()))
        self.back_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def validate_name(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.animal_name.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.animal_name.set("".join(text))

    def validate_special(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.special.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.special.set("".join(text))


# Hayvan silme sayfası
class DelAnimalPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.animal = tk.StringVar()
        self.animal.set("animal")

        self.select_animal_frame = tk.Frame(self)
        self.select_animal_frame.pack(fill="y", expand=True)

        self.animals_dropdown = ttk.Combobox(self.select_animal_frame, textvariable=self.animal,
                                             values=An.raw_animal_names)
        self.animals_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.select_animal_lbl = tk.Label(self.select_animal_frame, text="Bir Hayvan Seçin")
        self.select_animal_lbl.pack(side=tk.BOTTOM, pady=5)

        self.del_animal_frame = tk.Frame(self)
        self.del_animal_frame.pack(fill="y", expand=True)

        self.del_button = tk.Button(self.del_animal_frame, text="Sil", height=3, width=5,
                                    command=lambda: master.check_to_del(self.animals_dropdown.get()))
        self.back_button = tk.Button(self.del_animal_frame, text="Geri", height=3, width=5,
                                     command=lambda: master.switch_frame(SpecialFuncsPage))
        self.del_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=5)


# Hayvanlara ekleyeceğimiz özelliği ekleme sayfası
class AddFeaturePage(tk.LabelFrame):
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)
        if master.feature_to_add:  # reset feature to add
            master.feature_to_add = ""
        if master.animal_number:  # reset animal number to add feature
            master.animal_number = 0

        self.feature_frame = tk.Frame(self)
        self.feature_frame.pack(fill="y", expand=True)

        self.feature = tk.StringVar()
        self.feature.trace_variable("w", self.validate)

        self.feature_lbl = tk.Label(self.feature_frame,
                                    text="Eklemek istediğiniz özelliği kısaca girin: ")
        self.feature_lbl.pack(side=tk.LEFT, pady=30, padx=10)

        self.feature_entry = tk.Entry(self.feature_frame, textvariable=self.feature, width=20)
        self.feature_entry.pack(side=tk.LEFT, pady=30, padx=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="y", expand=True)

        self.back_btn = tk.Button(self.button_frame, text="Geri", height=3, width=10,
                                  command=lambda: master.switch_frame(SpecialFuncsPage))
        self.add_btn = tk.Button(self.button_frame, text="Ekle", height=3, width=10,
                                 command=lambda: master.add_feature(self.feature_entry.get()))

        self.back_btn.pack(side=tk.LEFT, padx=10)
        self.add_btn.pack(side=tk.LEFT, padx=10)

    def validate(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.feature.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.feature.set("".join(text))


# Hayvanlara özellikleri ekleme sayfası
class AddFeatureToAnimalsPage(tk.LabelFrame):
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.feature_frame = tk.Frame(self)
        self.feature_frame.pack(fill="y", expand=True)

        self.feature = tk.StringVar()
        self.feature.trace_variable("w", self.validate)

        self.feature_lbl = tk.Label(self.feature_frame,
                                    text="{} hayvanının {} özelliği: ".format(An.raw_animal_names[master.animal_number],
                                                                              master.feature_to_add))
        self.feature_lbl.pack(side=tk.LEFT, pady=30, padx=10)

        self.feature_entry = tk.Entry(self.feature_frame, textvariable=self.feature, width=20)
        self.feature_entry.pack(side=tk.LEFT, pady=30, padx=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="y", expand=True)

        self.back_btn = tk.Button(self.button_frame, text="Ana menü", height=3, width=10,
                                  command=lambda: master.discard_features())
        self.add_btn = tk.Button(self.button_frame, text="Ekle", height=3, width=10,
                                 command=lambda: master.feature_to_animals(self.feature_entry.get()))

        self.back_btn.pack(side=tk.LEFT, padx=10)
        self.add_btn.pack(side=tk.LEFT, padx=10)

    def validate(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.feature.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.feature.set("".join(text))


# Hayvanın belli bir özelliğinin değiştirildiği sayfa
class ChangeFeaturePage(tk.LabelFrame):
    wrong_letters = {"ý": "ı", "ð": "ğ", "þ": "ş"}

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.animal = tk.StringVar()
        self.animal.set("animal")

        self.select_animal_frame = tk.Frame(self)
        self.select_animal_frame.pack(fill="y", expand=True)

        self.animals_dropdown = ttk.Combobox(self.select_animal_frame, textvariable=self.animal,
                                             values=An.raw_animal_names)
        self.animals_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.select_animal_lbl = tk.Label(self.select_animal_frame, text="Bir Hayvan Seçin")
        self.select_animal_lbl.pack(side=tk.BOTTOM, pady=5)

        self.feature = tk.StringVar()
        self.feature.trace_variable("w", self.validate)

        self.select_feature_frame = tk.Frame(self)
        self.select_feature_frame.pack(fill="y", expand=True)

        self.feature_show_btn = tk.Button(self.select_feature_frame, text="Göster", height=3, width=8,
                                          command=lambda: master.show_feature(self.animals_dropdown.get(),
                                                                              self.features_dropdown.get()))
        self.feature_show_btn.pack(side=tk.BOTTOM, pady=5)

        self.features_dropdown = ttk.Combobox(self.select_feature_frame, textvariable=self.feature,
                                              values=list(An.question_answers.keys()))
        self.features_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.select_features_lbl = tk.Label(self.select_feature_frame, text="Bir Özellik Seçin")
        self.select_features_lbl.pack(side=tk.BOTTOM, pady=5)

        self.new_feature = tk.StringVar()
        self.new_feature.set("")

        self.change_frame = tk.Frame(self)
        self.change_frame.pack(fill="y", expand=True)

        self.feature_entry = tk.Entry(self.change_frame, textvariable=self.new_feature, width=15)
        self.feature_entry.pack(side=tk.LEFT)

        self.change_btn = tk.Button(self.change_frame, text="Değiştir", height=3, width=8,
                                    command=lambda: master.change_or_not(self.animals_dropdown.get(),
                                                                         self.features_dropdown.get(),
                                                                         self.feature_entry.get()))
        self.back_btn = tk.Button(self.change_frame, text="Geri", height=3, width=8,
                                  command=lambda: master.switch_frame(SpecialFuncsPage))
        self.change_btn.pack(side=tk.LEFT, padx=5)
        self.back_btn.pack(side=tk.LEFT, padx=5)

    def validate(self, *args):  # yazarken yanlış gözüken harfleri anında düzeltir
        text = list(self.new_feature.get())
        for n in range(len(text)):
            if text[n] in self.wrong_letters.keys():
                text[n] = self.wrong_letters[text[n]]
        self.new_feature.set("".join(text))


# Nasıl Oynandığı anlatılan sayfa
class HowToPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        tk.Label(self, text="Nasıl Oynanır", bg="white", fg="blue", pady=10, padx=10).pack(pady=40)

        for sentence in An.startlist:
            tk.Label(self, text=sentence, pady=5, padx=5).pack()

        tk.Button(self, text="Ana Menüye Dön", padx=10, pady=10,
                  command=lambda: master.switch_frame(StartPage)).pack(pady=20)


# Çıkış yapma sayfası
class ExitPage(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)

        self.exit_lbl_frame = tk.Frame(self)
        self.exit_lbl_frame.pack(fill="both", expand=True)

        self.exit_lbl = tk.Label(self.exit_lbl_frame, text="Çıkmak mı istiyorsun gerçekten ?", pady=10)
        self.exit_lbl.pack(side=tk.BOTTOM)  # Do You Really Want To Quit?

        self.exit_btn_frame = tk.Frame(self)
        self.exit_btn_frame.pack(fill="y", expand=True)

        self.exit_yes_btn = tk.Button(self.exit_btn_frame, text="Evet", padx=10,
                                      command=master.exit)  # YES
        self.exit_no_btn = tk.Button(self.exit_btn_frame, text="Hayır", padx=10,
                                     command=lambda: master.switch_frame(StartPage))  # No

        self.exit_yes_btn.pack(side=tk.LEFT, padx=10)
        self.exit_no_btn.pack(side=tk.LEFT, padx=10)
        self.exit_no_btn.focus()


# Oyun başlatılıyor
if __name__ == "__main__":
    App = Game()
    App.mainloop()
