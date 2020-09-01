import random
import genanki
from textwrap import dedent

random.seed(125)

# Create Anki model
phrase_model = genanki.Model(
    random.randint(1 << 30, 1 << 31),
    'Portugues Frequency List',
    fields=[
        {'name': 'Phrase'},
        {'name': 'Word'},
        {'name': 'Part of Speech'},
        {'name': 'Picture'},
        {'name': 'Audio'},
        {'name': 'Phrase_with'},
    ],
    templates=[
        {
            'name': 'Picture2Word',
            'qfmt':  dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Phrase}}</div>
                """),
            'afmt': dedent("""\
                <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Phrase_with}}</div>
                """),
        },
        {
            'name': 'Word2Picture',
            'qfmt': dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
                  """),
            'afmt': dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Phrase}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                """)
        },
    ],
    css=""".card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}"""
)

verb_model = genanki.Model(
    random.randint(1 << 30, 1 << 31),
    'verb trainer',
    fields=[
        {'name': 'Phrase'},
        {'name': 'Word'},
        {'name': 'Part of Speech'},
        {'name': 'Picture'},
        {'name': 'Audio'},
        {'name': 'Phrase_with'},
    ],
    templates=[
        {
            'name': 'Picture2Word',
            'qfmt':  dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Phrase}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                """),
            'afmt': dedent("""\
                <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Phrase_with}}</div>
                """),
        }, ],
    css=""".card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}"""
)

word_model = genanki.Model(
    random.randint(1 << 30, 1 << 31),
    'Portugues Frequency List',
    fields=[
        {'name': 'Word'},
        {'name': 'Part of Speech'},
        {'name': 'Picture'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Picture2Word',
            'qfmt':  dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
                """),
            'afmt': dedent("""\
                <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
                <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                """),
        },
        {
            'name': 'Word2Picture',
            'qfmt': dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
                  """),
            'afmt': dedent("""\
              <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Word}}</div>
              <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                """)
        },
    ],
    css=""".card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}"""
)
