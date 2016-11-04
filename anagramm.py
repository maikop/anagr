from pyvabamorf import analyze
from collections import defaultdict

min_pikkus = 4

def sobivad(fail, sisend):      ### Leiab sõnastikust sobivad sõnad
    sobivad = []
    for rida in fail:
        rida = rida.strip()
        if sisaldab(sisend, rida) is not None:
            if len(sisend) >= len(rida):
                sobivad.append(rida)
    return sorted(sobivad, key=len, reverse=True)

# kas sisend sisaldab seda sõna?
# kui sisaldab, siis eemaldab sisendist selle sõna tähed
def sisaldab(sisend, sona):
    if len(sisend) >= len(sona):
        sona = sona.strip().lower()
        while sona:
            taht, sona = sona[0:1] , sona[1:]
            if taht not in sisend:
                return None
            sisend = sisend.replace(taht, '', 1)    ### eemaldab kasutatud tähe
        return sisend                           ### ülejäänu

def sona(sisend,s):                        ### kas on sõna?
    if len(sisend) >= len(s):    ### kas on lühem kui sisend
        if s:
            if analyze(s, guess=False, phonetic=False,compound=False)[0]['analysis']: # on sõna?
                if sisaldab(sisend,s):      ### kui kõik uue sõna tähed sisalduvad sisendis
                    return True

def sonad(sisend, jj): ### jj - järjendite järjend
    verbs, sufs, prefs, noms, mms, lopps = jj[0], jj[1], jj[2], jj[3], jj[4], jj[5]
    sd = defaultdict(list)
    for pref in prefs+['']:
        for n in noms+['']:
            uus1 = pref+n           ### liida prefiks ja tüvi
            if sona(sisend, uus1):  ### kui uus sõna on analüsaatori arvates sõna
                if len(uus1) >= min_pikkus: ### ja uus sõna on pikem miinimumpikkusest
                    s = sd[''.join(sorted(uus1))]
                    a = set(s)
                    a.add(uus1)
                    sd[''.join(sorted(uus1))] = list(a)      ### lisa sobivate sõnade loendisse
                for suf in sufs+['']:       ### liida uuele sõnale suffiks
                    uus2 = uus1+suf         ### ja nii edasi
                    if sona(sisend, uus2):
                        if len(uus2) >= min_pikkus:
                            s = sd[''.join(sorted(uus2))]
                            a = set(s)
                            a.add(uus2)
                            sd[''.join(sorted(uus2))] = list(a)
                        for lopp in lopps+['']:
                            uus = uus2 + lopp
                            if sona(sisend, uus):
                                if len(uus2) >= min_pikkus:
                                    s = sd[''.join(sorted(uus))]
                                    a = set(s)
                                    a.add(uus)
                                    sd[''.join(sorted(uus))] = list(a)
        for v in verbs+['']:
            uus1 = pref+v           ### liida prefiks ja tüvi
            if sona(sisend, uus1):  ### kui uus sõna on analüsaatori arvates sõna
                if len(uus1) >= min_pikkus: ### ja uus sõna on pikem miinimumpikkusest
                    s = sd[''.join(sorted(uus1))]
                    a = set(s)
                    a.add(uus1)
                    sd[''.join(sorted(uus1))] = list(a)      ### lisa sobivate sõnade loendisse
                for suf in sufs+['']:       ### liida uuele sõnale suffiks
                    uus2 = uus1+suf         ### ja nii edasi
                    if sona(sisend, uus2):
                        if len(uus2) >= min_pikkus:
                            s = sd[''.join(sorted(uus2))]
                            a = set(s)
                            a.add(uus2)
                            sd[''.join(sorted(uus2))] = list(a)
                        for lopp in lopps+['']:
                            uus = uus2 + lopp
                            if sona(sisend, uus):
                                if len(uus2) >= min_pikkus:
                                    s = sd[''.join(sorted(uus))]
                                    a = set(s)
                                    a.add(uus)
                                    sd[''.join(sorted(uus))] = list(a)
        for m in mms+['']:
            uus1 = pref+m           ### liida prefiks ja tüvi
            if sona(sisend, uus1):  ### kui uus sõna on analüsaatori arvates sõna
                if len(uus1) >= min_pikkus: ### ja uus sõna on pikem miinimumpikkusest
                    s = sd[''.join(sorted(uus1))]
                    a = set(s)
                    a.add(uus1)
                    sd[''.join(sorted(uus1))] = list(a)      ### lisa sobivate sõnade loendisse
                for suf in sufs+['']:       ### liida uuele sõnale suffiks
                    uus2 = uus1+suf         ### ja nii edasi
                    if sona(sisend, uus2):
                        if len(uus2) >= min_pikkus:
                            s = sd[''.join(sorted(uus2))]
                            a = set(s)
                            a.add(uus2)
                            sd[''.join(sorted(uus2))] = list(a)
                        for lopp in lopps+['']:
                            uus = uus2 + lopp
                            if sona(sisend, uus):
                                if len(uus2) >= min_pikkus:
                                    s = sd[''.join(sorted(uus))]
                                    a = set(s)
                                    a.add(uus)
                                    sd[''.join(sorted(uus))] = list(a)
    return sd

    
def anagrammid(sisend, sonad, min_pikkus, sonadedict):
# leiab sisendile mitmesõnalised anagrammid,
# mis koosnevad vähemalt min_pikkusega sõnadest
    i = 0
    for sona in sonad:
        yle = sisaldab(sisend, sona)
        if yle == '':           ### Sõna ongi anagramm
            yield sona
        elif yle is not None and len(yle) >= min_pikkus:
            for j in anagrammid(yle, sonad[i:], min_pikkus, sonadedict):
                if not sonadedict[j]:
                    yield (' + '.join((' '.join(sonadedict[sona]), ' '.join([j]))))
                else:
                    yield (' + '.join((' '.join(sonadedict[sona]), ' '.join(sonadedict[j]))))
        i += 1
        
def main(sisend):
    sisend = sisend.lower().strip().replace(' ','').replace('-','')
    tykid = ['verb.ok', 'suf.ok', 'pref.ok', 'nomm.ok', 'mmm.ok', 'lopud.ok']
    s_tykid = []                ### Kõik sobilikud tykid
    for sonastik in tykid:
        with open(sonastik) as f:
            s_tykid.append(sobivad(f, sisend))   ### Sobilikud tükid
    sonu = 1
    sonadd = sonad(sisend, s_tykid)
    
    for sona in anagrammid(sisend, list(sonadd.keys()), min_pikkus, sonadd):
        print(str(sonu) + '. ' + sona)
        sonu += 1

print("\nSisesta väljumiseks 'q'")
sisend = input('või sisesta sõna(d): ')
while sisend != 'q':
    main(sisend)
    sisend = input('\n Sisesta sõnad: ')
