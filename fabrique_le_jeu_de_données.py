import os, shutil, csv

import html2markdown

from lawfactory_utils.urls import download
from tlfp.tools._step_logic import get_previous_step, use_old_procedure


def article_to_markdown(art):
    texte = ""
    for key in sorted(art["alineas"].keys()):
        if art["alineas"][key] != "":
            texte += art["alineas"][key] + "\n\n"
    return texte


def amendement_to_markdown(texte):
    return html2markdown.convert(texte)


dossiers = download(f"https://www.lafabriquedelaloi.fr/api/dossiers.csv")

for csv_dos in csv.DictReader(dossiers.text.splitlines(), delimiter=";"):
    law = csv_dos['id']
    dos = download(f"https://www.lafabriquedelaloi.fr/api/{law}/viz/procedure.json").json()

    for step_index, step in enumerate(dos["steps"]):
        if step.get("nb_amendements", 0) > 0:
            amendements = download(f"https://www.lafabriquedelaloi.fr/api/{law}/viz/amendements_{step['directory']}.json").json()
            try:
                texte = download(f"https://www.lafabriquedelaloi.fr/api/{law}/procedure/{step['directory']}/texte/texte.json").json()
            except:
                print('no texte')
                continue
            # recuperer le texte de l'etape precedente
            old_proc = use_old_procedure(step, dos)
            prev_step_index = get_previous_step(dos["steps"], step_index, old_proc)
            prev_step = dos["steps"][prev_step_index]

            try:
                prev_texte = download(f"https://www.lafabriquedelaloi.fr/api/{law}/procedure/{prev_step['directory']}/texte/texte.json").json()
            except:
                print('no prev texte')
                continue
            # pour chaque article
            for article in prev_texte["articles"]:
                article_title = "Article " + article["titre"]
                article_amendements = amendements["sujets"].get(article_title)
                if article_amendements:
                    # recuperer les amendements adoptés de l'article
                    article_amendements = [amdt for amdt in article_amendements["amendements"] if amdt["sort"] == "adopté"]
                    print('article:', article_title, len(article_amendements))
                    if article_amendements:
                        # pour chaque amendement recuperer le dispositif de l'amendement
                        try:
                            for amdt in article_amendements:
                                amdt['json'] = download(f"{amendements['api_root_url']}{amdt['id_api']}/json?{amdt['date']}").json()['amendement']
                        except:
                            print('one amendement request failed')
                            continue
                        # recuperer la prochaine version de l'article

                        next_article = None
                        for next_article_maybe in texte["articles"]:
                            if next_article_maybe["titre"] == article["titre"]:
                                next_article = next_article_maybe
                        if next_article:
                            dos_id = dos.get('assemblee_id', dos['id'])
                            directory = f"{dos_id}__{step['directory']}__{article['titre'].replace(' ', '_')}"
                            output_dir = os.path.join("données", directory)
                            shutil.rmtree(output_dir, ignore_errors=True)
                            os.makedirs(output_dir)
                            open(os.path.join(output_dir, 'article_avant'), 'w').write(article_to_markdown(article))
                            open(os.path.join(output_dir, 'article_apres'), 'w').write(article_to_markdown(next_article))

                            amendements_textes = set()
                            for amdt in article_amendements:
                                amdt_txt = amendement_to_markdown(amdt["json"]["texte"])
                                if amdt_txt not in amendements_textes:
                                    amendements_textes.add(amdt_txt)
                                    open(os.path.join(output_dir, 'amendement_' + amdt["numero"]), 'w').write(amendement_to_markdown(amdt["json"]["texte"]))
