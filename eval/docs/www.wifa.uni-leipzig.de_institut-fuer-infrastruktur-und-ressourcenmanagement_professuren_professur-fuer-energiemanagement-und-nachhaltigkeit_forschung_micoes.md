---
url: "https://www.wifa.uni-leipzig.de/institut-fuer-infrastruktur-und-ressourcenmanagement/professuren/professur-fuer-energiemanagement-und-nachhaltigkeit/forschung/micoes"
title: "Universität Leipzig: MICOES"
---

MICOES-Europe und MICOES-Barometer sind fundamentale Strommarktmodelle. MICOES-Europe bildet den europäischen Strommarkt detailliert ab und liefert Szenarien zukünftiger Day-ahead Strompreise unter Berücksichtigung verschiedener fundierter Annahmen. MICOES-Barometer fokussiert sich auf den deutschen Regelleistungsmarkt und berechnet fundamentale Leistungs- und Arbeitspreise für Primär-, Sekundär- und Minutenreserve (FCR, aFRR und mFRR).

**Software:** GAMS

**Modelltyp:** Techno-ökonomisch, deterministisch

**Einsatzgebiet:** Szenarien zukünftiger Strompreise (Day-ahead), Regelleistungspreise, optimaler Dispatch von Stromanbietern und -nachfragern

## Modellbeschreibung

#### Hintergrund

Die Preise am Großhandelsstrommarkt ändern sich zukünftig durch den weiteren Ausbau erneuerbarer Energien und die zunehmende Durchdringung mit Sektorkopplungstechnologien. Für Investitionsentscheidungen in neue Stromerzeugungs- oder -verbrauchsanlagen ist die Kenntnis der zukünftigen Entwicklung der Strompreise im Sinne von Erlösen oder Kosten zentral. Aufgrund des sich verändernden Kraftwerksparks können historische Preise aber nicht einfach in die Zukunft extrapoliert werden, da deren Struktur fundamentalen Änderungen unterliegt.

#### Modellierungsziel

Die fundamentalen Modelle MICOES-Europe und MICOES-Barometer setzen an dieser Stelle an und berücksichtigen explizit die techno-ökonomischen Eigenschaften des Kraftwerksparks sowie von flexiblen und inflexiblen Sektorkopplungstechnologien. Damit kann deren kostenoptimaler Einsatz am Strommarkt (Day-ahead und für Regelleistung) für zukünftige Szenarien ermittelt werden. Die Modelle liefern im Ergebnis Szenarien zukünftiger Day-ahead Strompreise sowie fundamentale Leistungs- und Arbeitspreise für FCR, aFRR und mFRR.

#### Ansatz

Beide Modelle nutzen eine detaillierte Datenbank des europäischen bzw. deutschen Kraftwerksparks mit seinen techno-ökonomischen Parametern. Zusätzlich werden stündlich aufgelöste Zeitreihen der herkömmlichen Stromnachfrage sowie von Wärmepumpen und Elektrofahrzeugen berücksichtigt. Die wetterabhängige Einspeisung von erneuerbaren Energien wird auf der Grundlage von regionalen Wetterdaten fundamental bestimmt. Beide Modelle berechnen den kostenoptimalen Anlageneinsatz als gemischt-ganzzahliges Optimierungsproblem und liefern im Ergebnis sowohl den Anlageneinsatz als auch Preise für Strom am Großhandelsmarkt bzw. Leistungs- und Arbeitspreise am Regelleistungsmarkt. Strategisches Verhalten wird in den Modellen nicht berücksichtigt.

#### Nutzen

Die Szenarien zukünftiger Preise für Strom am Großhandelsmarkt bzw. am Regelleistungsmarkt können als Unterstützung für Strategieentscheidungen eingesetzt werden. Insbesondere durch eine Variation der untersuchten Szenarien auf deren Auswirkungen lassen sich Sensitivitäten auf bestimmte Parameter im Voraus abschätzen.

## Eindrücke aus der Modellierung

vorheriges Element

Angezeigt wird Element 1 von 5

[![zur Vergrößerungsansicht des Bildes: ](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/b/a/csm_MICOES-Europe_Uebersicht_3a3d00f47c.png)](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Infrastruktur_und_Ressourcenmanagement/Energiemanagement_und_Nachhaltigkeit/3_Forschung/Modelle/MICOES/MICOES-Europe_Uebersicht.png)

Modellschema MICOES-Europe. Grafik: Böttger

[![zur Vergrößerungsansicht des Bildes: Vier einzelne Diagramme zeigen die Ergebnisse der Validierung für Beispielwochen der jahre 2010, 2011, 2021 und 2013. Die vom Modell berechneten Preise replizieren gut die Preise, die an der European Energy Exchange erzielt wurden. In den Jahren 2010, 2011 und 2012 ist eine leichte Überschätzung der Preise zu Zeiten mit niedriger Nachfrage, in den Jahren 2011 und 2013 eine leichte Unterschätzung der Preise in Zeiten mit hoher Nachfrage erkennbar. ](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/5/2/csm_MICOES-Europe_Validierung_5048c8229a.png)](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Infrastruktur_und_Ressourcenmanagement/Energiemanagement_und_Nachhaltigkeit/3_Forschung/Modelle/MICOES/MICOES-Europe_Validierung.png)

Ergebnisse der Modellvalidierung der historischen Strompreise von MICOES-Europe. Grafik: Böttger

[![zur Vergrößerungsansicht des Bildes: Das Diagramm zeigt in verschiedenen Farben die Sportmarktpreise in €/MWh. Deutlich erkennbar sind die Preisspitzen morgens und mittags, und die niedrigen Preise in der Nacht, und die allgemein geringeren Preise am Wochenende.](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/9/d/csm_MICOES-Europe_Beispielergebnisse_02d77ae69e.png)](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Infrastruktur_und_Ressourcenmanagement/Energiemanagement_und_Nachhaltigkeit/3_Forschung/Modelle/MICOES/MICOES-Europe_Beispielergebnisse.png)

Beispielergebnisse für zukünftige Strompreise einer Durchschnittswoche berechnet mit MICOES-Europe. Grafik: Böttger

[![zur Vergrößerungsansicht des Bildes: Die Grafik stellt Modellannahmen zu Spotmarktpreisen, Kraftwerkskapazität und den Bedarf an Regelleistung, den Modellablauf, und die Form der Ergebnisse dar, die unterschiedliche Informationen je Bieter, die Gesamtkosten für Vorhaltung und Abruf, und die Marktpreise enthalten.](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/7/f/csm_MICOES-Barometer_Uebersicht_796822b1ca.png)](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Infrastruktur_und_Ressourcenmanagement/Energiemanagement_und_Nachhaltigkeit/3_Forschung/Modelle/MICOES/MICOES-Barometer_Uebersicht.png)

Modellschema MICOES-Barometer. Grafik: Böttger

[![zur Vergrößerungsansicht des Bildes: Dargestellt in einem Balkendiagramm die mittleren Leistungspreise für Regelleistung mit und ohne Batterien. Die Preise sind für das Szenario mit Batterien geringer als für das Szenario ohne Batterien.](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/1/0/csm_MICOES-Barometer_Beispielergebnisse_502422335a.png)](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Infrastruktur_und_Ressourcenmanagement/Energiemanagement_und_Nachhaltigkeit/3_Forschung/Modelle/MICOES/MICOES-Barometer_Beispielergebnisse.png)

Beispielergebnisse zukünftiger Regelleistungspreise für zwei Szenarien. Grafik: Böttger

nächstes Element

- 1 / 5
- 2 / 5
- 3 / 5
- 4 / 5
- 5 / 5

## Modellnutzende und -entwickelnde

vorheriges Element

Angezeigt wird Element 1 von 3

![ Philipp Lerch](https://www.wifa.uni-leipzig.de/fileadmin/_processed_/9/9/csm_Philipp_Lerche_privat_c0f9c417e8.jpg)

## Philipp  Lerch

Wiss. Mitarbeiter

Energiemanagement und Nachhaltigkeit

work Institutsgebäude

Grimmaische Straße 12, Raum I 430

04109 Leipzig

Telefon: work+49 341 97 - 33521

[E-Mail Schreiben](https://www.wifa.uni-leipzig.de/institut-fuer-infrastruktur-und-ressourcenmanagement/professuren/professur-fuer-energiemanagement-und-nachhaltigkeit/forschung/micoes# "E-Mail schreiben an lerch[at]wifa.uni-leipzig.de")

[Zum Profil](https://www.wifa.uni-leipzig.de/personenprofil/mitarbeiter/philipp-lerch)

[Zum Profil](https://www.wifa.uni-leipzig.de/personenprofil?tx_mkunileipzig%5BexternalId%5D=p-2038-8932&cHash=de614591ead43817bd134ea45f6c7fc4)

![Default Avatar](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/Images/Icons/avatar_default.svg)

### Dr. Diana Böttger

Ehemalige wiss. Mitarbeiterin

Universität Leipzig, Institut für Infrastruktur und Ressourcenmanagement, Professur für Energiemanagement und Nachhaltigkeit

work

[E-Mail Schreiben](https://www.wifa.uni-leipzig.de/institut-fuer-infrastruktur-und-ressourcenmanagement/professuren/professur-fuer-energiemanagement-und-nachhaltigkeit/forschung/micoes# "E-Mail schreiben an diana.boettger[at]wifa.uni-leipzig.de")

nächstes Element

## Das könnte Sie auch interessieren

Angezeigt wird Element 1 von 3

### Optimierungsmodell IRPopt

[mehr erfahren](https://www.wifa.uni-leipzig.de/institut-fuer-infrastruktur-und-ressourcenmanagement/professuren/professur-fuer-energiemanagement-und-nachhaltigkeit/forschung/irpopt "zum Optimierungsmodell IRPopt")

### European Energy Exchange (EEX)

[mehr erfahren](https://www.eex.com/de/ "zur EEX (Link öffnet neuen Tab)")

### zurück zur Startseite der Professur

[mehr erfahren](https://www.wifa.uni-leipzig.de/institut-fuer-infrastruktur-und-ressourcenmanagement/professuren/professur-fuer-energiemanagement-und-nachhaltigkeit "zur Startseite der Professur")

![Eye-Able Logo](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able_whitelabel-icon_2.svg)

![Einstellungen zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-reset-top.svg)![Einstellungen öffnen](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/settings.png)

Eye-Able Assistenzsoftware Logo![Eye-Able Assistenzsoftware Logo](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able_whitelabel-icon_2.svg)![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-active-check.svg)[Eye-Able® Assistent](https://eye-able.com/)

![Eye-Able schließen und minimieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-circle-x.svg)![Info-Fenster öffnen](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-info.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Schnellmodus.svg)Sofortansicht![Speichern der Sofortansicht](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Save.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Font-Size.svg)Schriftgröße![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-Able-chevron-down.svg)

![Lupe Funktion](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-lupe.svg)0

![Schrifgröße verkleinern](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-minus.svg)![Schriftgröße zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-main-zoom-reset.svg)![Schriftgröße vergrößern](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-plus.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eyeable-right-arrow.svg) Mehr Einstellungen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Kontrastmodus.svg)Kontrastmodus![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-reset-top.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eyeable-right-arrow.svg) Mehr Farben.

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Bluefilter.svg)Blaufilter aktivieren

Intensität

80%

![Blaufilter reduzieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/bluefilter_minusRanger.svg)![Blaufilter verstärken](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/bluefilter_plusRanger.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Nightmode.svg)Nachtmodus

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Vorlesen.svg)Webseite vorlesen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Keyboard.svg)Tab Navigation

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Farbschwaeche.svg)Farbschwäche

Intensität

80%

![Farbfilter reduzieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/minusRanger.svg)![Farbfilter zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-main-zoom-reset.svg)![Farbfilter verstärken](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/plusRanger.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Image.svg)Bilder ausblenden

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-BigCursor.svg)Mauszeiger vergrößern

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Animation.svg)Animationen stoppen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-More-Functions.svg)Mehr Funktionen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-reset.svg)Alles zurücksetzen

➜ Eye-Able für mich ausblenden

Seite visuell anpassen!

Steuerungshilfe: