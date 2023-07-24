# Veszpremi kaják

Kigyűjti a környékbeli kajáldák aktuális napi, heti ajánlatait és kiküldi
Slack-en.
Első használat, függőségek telepítése:

```
poetry install
```

Illetve szükséges egy .env fájl (vagy a SLACK_TOKEN, CHANNEL_ID környezeti változók beállítása).

Használata:

```
poetry run python chatbot_main.py
```

És a felbukkanó Firefox böngészőben ki kell nyomni a sütik elfogadását,
illetve a bejelentkezés párbeszéd ablakát (elég az X, nem kell bejelentkezni).