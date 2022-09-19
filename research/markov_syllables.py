# import itertools
from decimal import Decimal

import black
import eng_to_ipa as ipa
import epitran
import evans
# from epitran.backoff import Backoff
from ipapy import is_valid_ipa
from ipapy.ipastring import IPAString
from nltk import tokenize

### From Corpus

corpus = "A. M. M. N. No. Na. Me. A. E. The Sea."
print(corpus)
print("")
split_corpus = tokenize.sent_tokenize(corpus)

converted_corpus = []

for sentence in split_corpus:
    # translated_sentence = ipa.ipa_list(sentence) # gives pronunsiation options
    translated_sentence = ipa.convert(sentence)  # chooses pronunciation
    converted_corpus.append(translated_sentence)

## ADD IPA BY HAND AS DESIRED:
# converted_corpus.append("əˈkiːn æˌkænˈθɑ.lə.d͡ʒi.")
converted_corpus.append(
    "al di la di sei fiumi e tre katene di montaɲe sord͡ʒe sora, t͡ʃitːa ke ki la vista una volta non puɔ piu dimentikare."
)  # Al di là di sei fiumi e tre catene di montagne sorge Zora, città che chi l'ha vista una volta non può piú dimenticare. Chi sei? Quale città? In cui si? -> beyond six rivers and three mountain ranges rises Zora, a city that no one, having seen it, can forget.
converted_corpus.append(
    "kosikːe ʎ uomini piu sapienti del mondo sono kuelːi ke sanːo a mente sora. ma inutilmente mi sono mesːo in viad͡ʒːo per visitare la t͡ʃitːa obːliɡata a restare imːobile e uɡuale a se stesːa per esːere meʎo rikordata, sora lanɡui, si disfet͡ʃe e ʃomparve. la terːa la dimentikata."
)  # Cosicché gli uomini piú sapienti del mondo sono quelli che sanno a mente Zora. Ma inutilmente mi sono messo in viaggio per visitare la città: obbligata a restare immobile e uguale a se stessa per essere meglio ricordata, Zora languí, si disfece e scomparve. La Terra l'ha dimenticata. -> So the world's most leared men are those who have memorized Zora. But in vain I set out to visit the city: forced to remain motionless and always the same, in order to be more easily remembered, Zora has languished, disintegrated, disappeared. The earth has forgotten her.
converted_corpus.append("ki sei?")  # Chi sei -> who are you?
converted_corpus.append("kuale t͡ʃitːa?")  # Quale città? -> Which city?
converted_corpus.append("in kui si?")  # In cui si? -> Where?
# converted_corpus.append("aٕðaː kaːn ɣiːr qaːdr ʕlى aːlnuːm liːlaːaː") # إذا كان غير قادر على النوم ليلاا -> if he is unable to sleep at night
converted_corpus.append(
    "txiːl ʔanh iːsiːr fiː aːlʃuːaːrʕ"
)  # تخيل أنه يسير في الشوارع -> imagine he's walking the streets
converted_corpus.append("tðkr aːlʔamr")  # تذكر الأمر -> remember it
converted_corpus.append(
    "altmθaːl aːlnaːsk uːaːlʔasd"
)  # التمثال الناسك والأسد -> the hermit statue and the lion
# converted_corpus.append("alzqaːq aːlmuːٔdiː ʔilى aːlmrfʔa") # الزقاق المؤدي إلى المرفأ -> the alley leading to the harbor

corpus_str = str(converted_corpus)

blacked_corpus_str = black.format_str(corpus_str, mode=black.mode.Mode())

print(blacked_corpus_str)
print("")


### USING IPAPY

all_consonants_list = []
all_vowels_list = []

for sentence in converted_corpus:
    s_uni = sentence.replace("?", ".")
    s_uni = s_uni.replace("!", ".")
    s_uni = s_uni.replace(",", "")
    print(f"Sentence IPA: {s_uni}")
    print(f"VALIDITY: {is_valid_ipa(s_uni)}")
    print("")
    s_ipa = IPAString(unicode_string=s_uni)
    sentence_consonants = s_ipa.consonants
    sentence_vowels = s_ipa.vowels
    for consonant in sentence_consonants:
        all_consonants_list.append(consonant)
    for vowel in sentence_vowels:
        all_vowels_list.append(vowel)
print("")

all_consonants_set = set(all_consonants_list)
all_vowels_set = set(all_vowels_list)

print("vowels:")
for vowel in all_vowels_set:
    print(f"\t{vowel}")
print("")
print("consonants:")
for consonant in all_consonants_set:
    print(f"\t{consonant}")
print("")

### From Markov

total_generated_syllables = 14

## VOWELS
total_vowels = len(all_vowels_list)
vowel_prob = {}
for vowel in all_vowels_set:
    sub_probs = {}
    for t in all_vowels_set:
        sub_probs[t] = Decimal(all_vowels_list.count(t) / total_vowels)
    vowel_prob[vowel] = sub_probs

vowel_chain = evans.Sequence.markov(
    transition_prob=vowel_prob,
    first_state=all_vowels_list[0],
    length=total_generated_syllables,
    seed=7,
)

## CONSONANTS
total_consonants = len(all_consonants_list)
consonant_prob = {}
for consonant in all_consonants_set:
    sub_probs = {}
    for t in all_consonants_set:
        sub_probs[t] = Decimal(all_consonants_list.count(t) / total_consonants)
    consonant_prob[consonant] = sub_probs

consonant_chain = evans.Sequence.markov(
    transition_prob=consonant_prob,
    first_state=all_consonants_list[0],
    length=total_generated_syllables,
    seed=7,
)


syllables = [f"{x}{y}" for x, y in zip(consonant_chain, vowel_chain)]

print("GENERATED SYLLABLES:")
for syllable in syllables:
    print(f"\t{syllable}")
print("")

# print("SYLLABLE COMBINATIONS")
# min_length = 2
# max_length = 3
# for i in range(min_length, max_length + 1):
#     print(f"COMBINATIONS OF SIZE {i}:")
#     for combination in itertools.combinations(syllables, i):
#         printable_combination = ""
#         for sub_unit in combination:
#             printable_combination += sub_unit + "-"
#         print(f"\t{printable_combination}")


print("")

### WITH EPITRAN

epi_persian = epitran.Epitran("uig-Arab")  # Uyghur in Perso-Arabic script

epi_farsi = epitran.Epitran("fas-Arab")  # farsi

epi_arabic = epitran.Epitran("ara-Arab")  # literary arabic

epi_german = epitran.Epitran("deu-Latn")  # german

epi_hindi = epitran.Epitran("hin-Deva")  # hindi

epi_italian = epitran.Epitran("ita-Latn")  # italian

epi_spanish = epitran.Epitran("spa-Latn")  # spanish

epi_urdu = epitran.Epitran("urd-Arab")  # urdu

epi_french = epitran.Epitran("fra-Latn")  # french

epi_english = epitran.Epitran("eng-Latn")  # english


print("GERMAN")
german_test = epi_german.transliterate("schwefelhölzern")
print(german_test)
print("")

print("HINDI")
hindi_test = epi_hindi.transliterate("हिन्दी")
print(hindi_test)
hindi_test_2 = epi_hindi.trans_list("हिन्दी")
print(hindi_test_2)
print("")

print("URDU")
urdu_test = epi_urdu.transliterate("سشات")
print(urdu_test)
urdu_test_2 = epi_urdu.transliterate("تحوت")
print(urdu_test_2)
urdu_test_3 = epi_urdu.transliterate("ماعت")
print(urdu_test_3)
print("")

print("LITERARY ARABIC")
arabic_test = epi_arabic.transliterate("سشات")
print(arabic_test)
arabic_test_2 = epi_arabic.transliterate("تحوت")
print(arabic_test_2)
arabic_test_3 = epi_arabic.transliterate("ماعت")
print(arabic_test_3)
print("ARABIC FOR OPERA")
arabic_test_4_1 = epi_arabic.transliterate(
    "إذا كان غير قادر على النوم ليلاا"
)  # if he is unable to sleep at night
arabic_test_4_2 = epi_arabic.transliterate(
    "تخيل أنه يسير في الشوارع"
)  # imagine he's walking the streets
arabic_test_4_3 = epi_arabic.transliterate("تذكر الأمر")  # remember it
arabic_test_4_4 = epi_arabic.transliterate(
    "التمثال الناسك والأسد"
)  # the hermit statue and the lion
arabic_test_4_5 = epi_arabic.transliterate(
    "الزقاق المؤدي إلى المرفأ"
)  # the alley leading to the harbor
print(arabic_test_4_1)
print(arabic_test_4_2)
print(arabic_test_4_3)
print(arabic_test_4_4)
print(arabic_test_4_5)
print("")

print("PERSIAN")
farsi_test = epi_farsi.transliterate("سشات")
print(farsi_test)
farsi_test_2 = epi_farsi.transliterate("تحوت")
print(farsi_test_2)
farsi_test_3 = epi_farsi.transliterate("ماعت")
print(farsi_test_3)
farsi_test_4 = epi_farsi.transliterate(
    """
    در ورای شش رودخانه و سه رشته کوه زورا، شهری که هیچ کس در آن نیست
با دیدن آن، می تواند فراموش کند. اما نه به این دلیل که، مانند دیگر شهرهای به یاد ماندنی، آن را
تصویری غیرعادی در خاطرات شما به جا می گذارد. زورا دارای کیفیت است
نقطه به نقطه در خاطرات شما باقی می ماند، در خیابان های متوالی آن، از
هر چند خانه های کنار خیابان ها و در و پنجره ها در خانه ها
هیچ چیز در آنها زیبایی یا کمیاب خاصی ندارد. راز زورا در
همانطور که در یک موزیکال نگاه شما بر روی الگوهایی که پشت سر هم قرار می گیرند می گذرد
امتیازی که در آن یک یادداشت قابل تغییر یا جابجایی نیست. مردی که می داند توسط
قلب چگونه ساخته شده زورا، اگر او نمی تواند در شب بخوابد، می تواند تصور کند که او است
راه رفتن در امتداد خیابان ها و او به یاد نظم است که توسط مس
ساعت به دنبال سایه بان راه راه آرایشگر و سپس فواره با نه می رود
جت ها، برج شیشه ای ستاره شناس، کیوسک خربزه فروش، مجسمه
گوشه نشین و شیر، حمام ترکی، کافه گوشه، کوچه
که به بندر منتهی می شود شهری که نمی توان آن را از ذهن پاک کرد
مانند یک آرماتور است، یک لانه زنبوری که هر یک از ما می توانیم آن را در سلول های آن قرار دهیم
چیزهایی که او می خواهد به خاطر بسپارد: نام مردان مشهور، فضایل، اعداد،
طبقه بندی سبزیجات و مواد معدنی، تاریخ نبردها، صور فلکی، قطعات
از گفتار بین هر ایده و هر نقطه از برنامه سفر یک قرابت یا یک
کنتراست را می توان ایجاد کرد و به عنوان یک کمک فوری به حافظه عمل می کند. بنابراین
دانشمندترین مردان جهان کسانی هستند که زورا را حفظ کرده اند.
اما بیهوده به دیدار شهر رفتم: مجبور شدم بی حرکت بمانم و
زورا همیشه همینطور است، برای اینکه راحت‌تر به خاطر بسپارید
از بین رفت، متلاشی شد، ناپدید شد. زمین او را فراموش کرده است.
    """
)
print(farsi_test_4)
print("")

# print("ENGLISH") # only use eng-to-ipa
# english_test = epi_english.transliterate(u'hello')
# print(english_test)
# print("")

print("SPANISH")
spanish_test = epi_spanish.transliterate(
    "Me gustas cuando callas porque estás como ausente, y me oyes desde lejos, y mi voz no te toca. Parece que los ojos se te hubieran voldado. Como todas las cosas están llenas de mi alma, emerges de las cosas, llena del alma mía. Déjame que te hable también con tu silencio."
)  # i like it when you're quiet. it's as if you weren't here now, and you heard me from a distance, and my voice couldn't reach you. it's as if your eyes had flown away from you. just as all living things are filled with my soul, you emerge from all living things filled with the soul of me. it's then that what i want is to speak to your silence. (neruda - twenty love poems 15)
print(spanish_test)
spanish_test_2 = epi_spanish.transliterate(
    "Como cenizas, como mares poblándose, en la sumergida lentitud, en lo informe, o como se oyen desde el alto de los caminos cruzar las campanadas en cruz, teniendo ese sonido ya aparte del metal, confuso, pesado, haciéndose polvo en el mismo molino de las formas demasiado lejos, o recordadas o no vistas ..."
)  # Like ashes, like oceans gathering themselves, in the submerged slowness, in what's unformed, or like hearing from a high place on the road the cross-echo of church bells, holding that sound just off the metal, confused, weighing down, turning to dust, in the same mill of forms, too far away, remembered or never seen ... (neruda - dead gallop)
print(spanish_test_2)
spanish_test_3 = epi_spanish.transliterate(
    "Me rodea una misma cosa, un solo movimiento: el peso del mineral, la luz de la piel, se pegan al sonido de la palabra noche ... Trabajo sordamente, girando sobre mí mismo, como el cuervo sobre la muerte, el cuervo de luto ... central, rodeado de geografía silenciosa ..."
)  # Just one thing surrounds me, a single motion: the weight of rocks, the light of skin, fasten themselves to the sound of the word night ... I toil deafly, circling above myself, like a raven above death, grief's raven ... dead center, surrounded by silent geography ... (neruda - oneness)
print(spanish_test_3)
spanish_test_4 = epi_spanish.transliterate(
    "y apenas sostenidos por el aire y por los sueños"
)  # and barely kept alive by air and by dreams (neruda - system of gloom)
print(spanish_test_4)
spanish_test_5 = epi_spanish.transliterate(
    "Hay cementerios solos, tumbas llenas de huesos sin sonido, el corazón pasando un túnel oscuro, oscuro, oscuro, como un naufragio hacia adentro nos morimos, como ahogarnos en el corazón, como irnos cayendo desde la piel al alma. ... a lo sonoro llega la muerte ... Yo no sé, yo conozco poco, yo apenas veo, ... sopla un sonido oscuro que hinch sábanas, y hay camas navegando a un puerto en donde está esperando, vestida de almirante. Sí. El sí."
)  # There are lone cemetaries, tombs filled with mute bones, the heart going through a tunnel. shadowy, shadowy, shadowy: we die as if a ship were going down inside us, like a drowning in the heart, like falling endlessly from the skin to the soul. ... It's sound that death is drawn to ... I don't know, I understand so little, I can hardly see ... blows a dark sound that swells the sheets and beds are sailing into a harbor where death is waiting, dressed as an admiral (neruda - only death)
print(spanish_test_5)
print("")

print("ITALIAN")
italian_test = epi_italian.transliterate(
    "Al di là di sei fiumi e tre catene di montagne sorge Zora, città che chi l'ha vista una volta non può piú dimenticare. Chi sei? Quale città? In cui si?"
)
print(italian_test)
italian_test_2 = epi_italian.transliterate(
    "Cosicché gli uomini piú sapienti del mondo sono quelli che sanno a mente Zora. Ma inutilmente mi sono messo in viaggio per visitare la città: obbligata a restare immobile e uguale a se stessa per essere meglio ricordata, Zora languí, si disfece e scomparve. La Terra l'ha dimenticata."
)
print(italian_test_2)
print("")

print("FRENCH")
french_test = epi_french.transliterate("saison")
print(french_test)
print("")
