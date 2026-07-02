"""
Curadoria do catálogo Metalab (fonte: análise visual das embalagens +
fichas técnicas de data/imports/fichas-tecnicas do projeto original).

- MAXMA_REMOVER: produtos com a marca MAXMA impressa na embalagem (saem da loja).
- LINHA_INOVITANN: produtos da linha Inovitann Clinical (seção própria).
- CATEGORIAS: taxonomia correta, com ordem de exibição.
- CATALOGO: por produto base -> categoria, conteúdo SEO/GEO/AEO
  (o comando `reorganizar_catalogo` monta descrições e aplica aos kits).
"""

# ─── Produtos MAXMA (identificados pela logomarca na embalagem) ──────────────
MAXMA_REMOVER = [
    "Ademoril", "Cogplene", "Dermatrox", "Laxmovi PEG", "Melasun", "Movelev",
    "Movilac 120ml", "Movilac 200ml", "Pankreoflat", "Peadex 300", "Peadex 600",
    "Purofer 150mg", "Purofer 300mg", "Purofer Gotas",
    "Visyneral DHA", "Visyneral Folato", "Visyneral Pré-Natal", "Visyneral SOP",
]

# ─── Linha Inovitann Clinical (embalagens com a marca INOVITANN) ─────────────
LINHA_INOVITANN = [
    "Biotina", "Cloreto de Magnésio", "Metilcobalamina", "NAC", "Q10", "Vitamina K",
    "Cúrcuma", "LUT+ZEA", "Magnésio L-Treonina", "Penta Magnésio", "Trimagnésio",
]

# ─── Categorias corretas ─────────────────────────────────────────────────────
CATEGORIAS = [
    ("Vitaminas", "Vitaminas essenciais para energia, imunidade e metabolismo."),
    ("Ossos e Músculos", "Cálcio, HMB e nutrientes para ossos e massa muscular."),
    ("Articulações", "Colágeno tipo II, glucosamina e condroitina para a função articular."),
    ("Ferro e Anemia", "Suplementos de ferro de alta absorção."),
    ("Digestão e Fígado", "Enzimas digestivas, lactase e suporte hepático."),
    ("Intestino e Fibras", "Fibras, reguladores intestinais e probióticos."),
    ("Respiratório e Garganta", "Acetilcisteína, própolis e pastilhas para garganta."),
    ("Circulação", "Pinus pinaster para o conforto das pernas e circulação."),
    ("Sono e Cognição", "Maracujá, nootrópicos e suporte ao bem-estar mental."),
    ("Infantil", "Linha pediátrica: cólicas, apetite, vitaminas e probióticos."),
    ("Compostos Naturais", "Extratos vegetais e fitoterápicos tradicionais."),
    ("Dor e Febre", "Analgésicos e antitérmicos."),
    ("Linha Inovitann", "Inovitann Clinical: suplementos de alta pureza e dose otimizada."),
]

# ─── Conteúdo por produto base ───────────────────────────────────────────────
# Campos: cat, oque (o que é / para que serve), comp (composição resumida),
#         modo (modo de uso), faq (lista de (pergunta, resposta) — AEO)
CATALOGO = {
    "Água Inglesa": {
        "cat": "Digestão e Fígado",
        "oque": "suplemento alimentar líquido tradicional à base de quina (240ml), "
                "usado como tônico amargo para estimular o apetite e apoiar a digestão",
        "comp": "Água purificada, extrato de quina e cianocobalamina (vitamina B12).",
        "modo": "Tomar 1 colher de sopa (15ml) antes das principais refeições, ou conforme orientação profissional.",
        "faq": [
            ("Para que serve a Água Inglesa?",
             "É um tônico amargo tradicional usado para estimular o apetite e auxiliar a digestão, especialmente em períodos de fraqueza ou convalescença."),
            ("Água Inglesa abre o apetite?",
             "Sim, os princípios amargos da quina estimulam naturalmente as secreções digestivas, favorecendo o apetite."),
        ],
    },
    "Apetimax": {
        "cat": "Infantil",
        "oque": "suplemento vitamínico infantil em solução (240ml) com complexo B, "
                "vitamina C e poliaminoácidos, formulado para apoiar o apetite e o "
                "desenvolvimento das crianças",
        "comp": "Vitaminas do complexo B (B1, B2, B3, B5, B6, B12), vitamina C e aminoácidos essenciais.",
        "modo": "Crianças: 1 colher de sopa (15ml) ao dia, de preferência junto a uma refeição, ou conforme orientação do pediatra.",
        "faq": [
            ("Apetimax abre o apetite infantil?",
             "O Apetimax BC combina vitaminas do complexo B, vitamina C e aminoácidos que participam do metabolismo energético, apoiando o apetite e a disposição das crianças."),
            ("A partir de que idade pode usar?",
             "Uso pediátrico conforme orientação do pediatra ou nutricionista."),
        ],
    },
    "Articulice": {
        "cat": "Articulações",
        "oque": "suplemento alimentar em comprimidos com colágeno tipo II não "
                "desnaturado (UC-II 40mg), ácido hialurônico e glucosaminoglicanos "
                "da membrana da casca do ovo, que auxilia na manutenção da função articular",
        "comp": "Membrana da casca do ovo (colágeno tipo II não desnaturado 40mg, ácido hialurônico 5,3mg, glucosaminoglicanos 5,3mg), colágeno 28mg. 30 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água, de preferência sempre no mesmo horário.",
        "faq": [
            ("Qual a diferença do colágeno tipo II para o colágeno comum?",
             "O colágeno tipo II não desnaturado (UC-II) atua na cartilagem articular por mecanismo imunológico em doses pequenas (40mg), enquanto o colágeno hidrolisado comum precisa de doses de 10g ou mais."),
            ("Quanto tempo para sentir os efeitos nas articulações?",
             "Estudos com UC-II observam benefícios na função articular a partir de 90 dias de uso contínuo."),
        ],
    },
    "Articulice Cúrcuma": {
        "cat": "Articulações",
        "oque": "versão do Articulice enriquecida com extrato de cúrcuma (curcumina), "
                "combinando colágeno tipo II não desnaturado com o poder antioxidante "
                "da Curcuma longa para o conforto articular",
        "comp": "Colágeno tipo II não desnaturado (UC-II 40mg), membrana da casca do ovo e extrato seco de cúrcuma padronizado em curcuminoides.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("Por que combinar cúrcuma com colágeno tipo II?",
             "A curcumina tem ação antioxidante que complementa o mecanismo do UC-II na manutenção do conforto e da mobilidade articular."),
        ],
    },
    "Azigov": {
        "cat": "Ossos e Músculos",
        "oque": "suplemento efervescente em sachês de cálcio com vitaminas B9 (ácido "
                "fólico) e B12, sabor uva e limão, sem açúcar, de rápida absorção",
        "comp": "Cálcio, vitamina B9 (ácido fólico) e vitamina B12. Sachês efervescentes sabor uva e limão, sem açúcar.",
        "modo": "Dissolver 1 sachê em um copo de água (200ml) e tomar 1 vez ao dia.",
        "faq": [
            ("Para que serve o Azigov?",
             "Fornece cálcio para ossos e dentes junto com vitaminas B9 e B12, que participam da formação das células sanguíneas e do metabolismo energético."),
        ],
    },
    "Azigov Pote": {
        "cat": "Ossos e Músculos",
        "oque": "versão em pote (120g) do suplemento efervescente Azigov: cálcio com "
                "vitaminas B9 e B12, sabor uva e limão, sem açúcar",
        "comp": "Cálcio, vitamina B9 (ácido fólico) e vitamina B12 em pó efervescente. Pote 120g.",
        "modo": "Dissolver 1 medida em um copo de água e tomar 1 vez ao dia.",
        "faq": [
            ("Qual a diferença entre o Azigov sachê e o pote?",
             "A fórmula é a mesma; o pote de 120g rende mais doses e é mais econômico para uso contínuo."),
        ],
    },
    "Biotina": {
        "cat": "Linha Inovitann",
        "oque": "suplemento da linha Inovitann Clinical com Biotina Plus em cápsulas "
                "(150% da IDR), que contribui para a manutenção do cabelo, da pele e das unhas — "
                "sem açúcar, sem glúten e sem lactose",
        "comp": "Biotina (vitamina B7) — 150% da IDR por cápsula. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, com água.",
        "faq": [
            ("Biotina serve para cabelo e unhas?",
             "Sim. A biotina contribui para a manutenção do cabelo e da pele, e a suplementação apoia unhas mais fortes em pessoas com baixa ingestão."),
            ("Quanto tempo usar biotina?",
             "Ciclos de 3 a 6 meses são comuns; unhas e cabelos respondem no ritmo natural de crescimento."),
        ],
    },
    "Bisglicinato Ferroso 30": {
        "cat": "Ferro e Anemia",
        "oque": "suplemento de ferro bisglicinato quelato 150mg em comprimidos "
                "revestidos (30 unidades), forma de alta absorção e melhor tolerância "
                "gástrica, zero açúcar e sem glúten",
        "comp": "Ferro bisglicinato quelato 150mg por comprimido. 30 comprimidos revestidos.",
        "modo": "Tomar 1 comprimido ao dia, de preferência longe de café, chá e laticínios.",
        "faq": [
            ("Bisglicinato ferroso dá menos enjoo que sulfato ferroso?",
             "Sim, o ferro quelado ao aminoácido glicina tende a causar menos desconforto gástrico e prisão de ventre que os sais tradicionais."),
            ("Posso tomar ferro com vitamina C?",
             "Sim, a vitamina C aumenta a absorção do ferro; evite tomar junto com leite ou café."),
        ],
    },
    "Bisglicinato Ferroso 60": {
        "cat": "Ferro e Anemia",
        "oque": "embalagem econômica com 60 comprimidos de ferro bisglicinato quelato "
                "150mg, alta absorção e melhor tolerância gástrica, zero açúcar e sem glúten",
        "comp": "Ferro bisglicinato quelato 150mg por comprimido. 60 comprimidos revestidos.",
        "modo": "Tomar 1 comprimido ao dia, longe de café, chá e laticínios.",
        "faq": [
            ("Para quem é indicada a embalagem de 60 comprimidos?",
             "Para quem faz reposição contínua de ferro por 2 meses ou mais, com melhor custo por dose."),
        ],
    },
    "Camomila Baby": {
        "cat": "Infantil",
        "oque": "suplemento infantil em cápsulas com camomila, erva-doce e vitaminas, "
                "tradicionalmente usado para apoiar o conforto e a tranquilidade dos bebês",
        "comp": "Extratos de camomila e erva-doce, vitaminas C e D. 20 cápsulas (abrir e diluir).",
        "modo": "Uso pediátrico: conforme orientação do pediatra.",
        "faq": [
            ("Camomila ajuda o bebê a dormir?",
             "A camomila é tradicionalmente usada por seu efeito calmante suave, apoiando o relaxamento e o sono tranquilo dos pequenos."),
        ],
    },
    "Carve Active": {
        "cat": "Digestão e Fígado",
        "oque": "carvão vegetal ativado em cápsulas, que auxilia na redução de gases "
                "e do desconforto abdominal, apoiando o conforto digestivo",
        "comp": "Carvão vegetal ativado de alta porosidade em cápsulas.",
        "modo": "Tomar 1 a 2 cápsulas após as refeições ou ao sentir desconforto por gases.",
        "faq": [
            ("Carvão ativado serve para gases?",
             "Sim, o carvão ativado adsorve gases e compostos no trato digestivo, aliviando estufamento e flatulência."),
            ("Carvão ativado corta o efeito de remédios?",
             "Pode reduzir a absorção de medicamentos; tome com intervalo de pelo menos 2 horas."),
        ],
    },
    "Cloreto de Magnésio": {
        "cat": "Linha Inovitann",
        "oque": "Cloreto de Magnésio P.A. (pureza analítica) da linha Inovitann "
                "Clinical, 60 cápsulas — magnésio de alta solubilidade que participa de "
                "mais de 300 reações do organismo, dos músculos ao sistema nervoso",
        "comp": "Cloreto de magnésio hexahidratado grau P.A. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, com água, de preferência à noite.",
        "faq": [
            ("Para que serve o cloreto de magnésio?",
             "O magnésio atua em mais de 300 reações enzimáticas: função muscular, sistema nervoso, energia (ATP) e saúde óssea."),
            ("Qual a diferença do grau P.A.?",
             "P.A. significa 'pureza analítica' — matéria-prima com o mais alto grau de pureza, livre de contaminantes."),
        ],
    },
    "Cogniflex": {
        "cat": "Sono e Cognição",
        "oque": "fórmula avançada para performance cerebral com colina, magnésio, "
                "zinco, selênio, metionina e vitaminas do complexo B, D e E — 60 cápsulas "
                "para foco, memória e clareza mental",
        "comp": "Colina, bisglicinato de magnésio, malato de magnésio, bisglicinato de zinco, selênio, metionina, vitaminas do complexo B, D e E. 60 cápsulas.",
        "modo": "Tomar 2 cápsulas ao dia, de preferência pela manhã.",
        "faq": [
            ("Cogniflex é nootrópico?",
             "É um suplemento com nutrientes que participam da síntese de neurotransmissores e do metabolismo energético cerebral, apoiando foco e memória."),
        ],
    },
    "Complexo B": {
        "cat": "Vitaminas",
        "oque": "vitaminas do complexo B (B1, B2, B3, B5 e B6) em comprimidos "
                "revestidos, zero açúcar e sem glúten, para energia e metabolismo — 50 comprimidos",
        "comp": "Vitaminas B1 (tiamina), B2 (riboflavina), B3 (niacina), B5 (ácido pantotênico) e B6 (piridoxina). 50 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Para que serve o complexo B?",
             "As vitaminas B participam da transformação dos alimentos em energia, da saúde do sistema nervoso e da formação das células sanguíneas."),
        ],
    },
    "Complexo B Concentrado": {
        "cat": "Vitaminas",
        "oque": "versão concentrada do Complexo B em 20 comprimidos com doses "
                "reforçadas das vitaminas B1, B2, B3, B5 e B6",
        "comp": "Vitaminas do complexo B em doses concentradas. 20 comprimidos revestidos.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Quando escolher o Complexo B Concentrado?",
             "Quando há maior demanda energética, estresse físico ou orientação profissional para doses mais altas de vitaminas B."),
        ],
    },
    "Condroless": {
        "cat": "Articulações",
        "oque": "colágeno tipo II não desnaturado 40mg em comprimidos (60 unidades), "
                "que auxilia na manutenção da função articular",
        "comp": "Colágeno tipo II não desnaturado 40mg por comprimido. 60 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("Condroless substitui glucosamina?",
             "São mecanismos diferentes: o colágeno tipo II atua por tolerância imunológica na cartilagem, e pode ser usado como alternativa ou complemento à glucosamina."),
        ],
    },
    "Condroless Complex": {
        "cat": "Articulações",
        "oque": "colágeno tipo II não desnaturado com cúrcuma e vitamina C — fórmula "
                "completa para articulações com ação antioxidante (60 comprimidos)",
        "comp": "Colágeno tipo II não desnaturado, extrato de cúrcuma e vitamina C. 60 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("O que a vitamina C acrescenta à fórmula?",
             "A vitamina C participa da formação natural de colágeno pelo organismo, complementando a ação do colágeno tipo II."),
        ],
    },
    "Condroless Ultra": {
        "cat": "Articulações",
        "oque": "a fórmula mais completa da família Condroless: colágeno tipo II "
                "não desnaturado + MDK (magnésio, vitaminas D e K) para articulações e ossos "
                "(60 comprimidos)",
        "comp": "Colágeno tipo II não desnaturado 40mg, magnésio, vitamina D e vitamina K. 60 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("Por que o Condroless Ultra tem vitaminas D e K?",
             "D e K trabalham em conjunto na fixação do cálcio nos ossos, somando saúde óssea ao cuidado articular do colágeno tipo II."),
        ],
    },
    "Dissocal": {
        "cat": "Compostos Naturais",
        "oque": "suplemento alimentar em solução (150ml) com vitaminas A, C, E, zinco "
                "e extrato fluido de abacate, enriquecido com extratos vegetais tradicionais "
                "(abútua, caroba, chapéu de couro, quebra-pedra, sabugueiro)",
        "comp": "Vitamina A 600mcg, vitamina C 45mg, vitamina E, zinco 7mg, extrato fluido de abacate e extratos vegetais. 150ml.",
        "modo": "Tomar 30ml ao dia, ou conforme orientação profissional.",
        "faq": [
            ("O que é o Dissocal?",
             "Um polivitamínico líquido com antioxidantes (A, C, E e zinco) e extratos vegetais da tradição brasileira, como quebra-pedra e chapéu de couro."),
        ],
    },
    "Elixir Santa Raiz": {
        "cat": "Compostos Naturais",
        "oque": "elixir tradicional (240ml) saborizado com inhame e salsa, receita "
                "clássica usada como depurativo natural",
        "comp": "Extratos vegetais tradicionais, inhame e salsa. 240ml.",
        "modo": "Tomar 1 colher de sopa (15ml) 1 a 2 vezes ao dia.",
        "faq": [
            ("Para que serve o Elixir Santa Raiz?",
             "É um composto depurativo tradicional à base de plantas, usado para apoiar o bem-estar geral e a 'limpeza' do organismo."),
        ],
    },
    "Enzicoba": {
        "cat": "Vitaminas",
        "oque": "metilcobalamina (vitamina B12 ativa) em comprimidos mastigáveis com "
                "414% da IDR — alto teor de B12 que auxilia na formação das células vermelhas "
                "do sangue, sem açúcar e sem glúten (60 comprimidos)",
        "comp": "Metilcobalamina (vitamina B12 na forma ativa) — 414% da IDR por comprimido mastigável. 60 comprimidos.",
        "modo": "Mastigar 1 comprimido ao dia.",
        "faq": [
            ("Qual a vantagem da metilcobalamina sobre a cianocobalamina?",
             "A metilcobalamina é a forma ativa da B12, pronta para uso pelo organismo, sem necessidade de conversão."),
            ("Quem precisa suplementar B12?",
             "Vegetarianos, veganos, pessoas 50+, usuários de metformina ou omeprazol e quem tem absorção reduzida."),
        ],
    },
    "Epanon Amargo": {
        "cat": "Digestão e Fígado",
        "oque": "suplemento líquido (200ml) com colina, vitamina C e vitamina D — "
                "tônico amargo que apoia o metabolismo hepático e a digestão",
        "comp": "Colina, vitamina C e vitamina D em solução. 200ml.",
        "modo": "Tomar 1 colher de sopa (15ml) antes das refeições.",
        "faq": [
            ("Para que serve um tônico amargo?",
             "Amargos estimulam as secreções digestivas; a colina contribui para o metabolismo normal das gorduras no fígado."),
        ],
    },
    "Epatinon Comprimido": {
        "cat": "Digestão e Fígado",
        "oque": "cloreto de colina com metionina em comprimidos revestidos (30 "
                "unidades), que contribui para o metabolismo lipídico e a função hepática",
        "comp": "Cloreto de colina e metionina. 30 comprimidos revestidos.",
        "modo": "Tomar 1 comprimido 1 a 2 vezes ao dia, após as refeições.",
        "faq": [
            ("Para que serve colina + metionina?",
             "São nutrientes lipotrópicos: participam do transporte e do metabolismo das gorduras no fígado."),
        ],
    },
    "Epatinon Flaconete": {
        "cat": "Digestão e Fígado",
        "oque": "cloreto de colina, metionina e cianocobalamina (B12) em flaconetes "
                "de 10ml (60 unidades) — praticidade dose a dose para o metabolismo lipídico",
        "comp": "Cloreto de colina, metionina e cianocobalamina (B12). 60 flaconetes de 10ml.",
        "modo": "Tomar 1 flaconete ao dia, puro ou diluído em água.",
        "faq": [
            ("Qual a vantagem do flaconete?",
             "Dose líquida pronta, de absorção rápida, prática para levar na bolsa ou viagem."),
        ],
    },
    "Epatinon Xarope": {
        "cat": "Digestão e Fígado",
        "oque": "versão em solução oral (120ml) do Epatinon: colina, metionina e B12 "
                "para apoiar o metabolismo das gorduras e a função hepática",
        "comp": "Cloreto de colina, metionina e cianocobalamina (B12). Frasco 120ml.",
        "modo": "Tomar 1 colher de sopa (15ml) 1 a 2 vezes ao dia.",
        "faq": [
            ("Epatinon ajuda na digestão de comidas gordurosas?",
             "A colina e a metionina participam do metabolismo hepático das gorduras, apoiando a sensação de conforto após refeições pesadas."),
        ],
    },
    "Fleboderm": {
        "cat": "Circulação",
        "oque": "creme dermocosmético (250ml) para pernas cansadas, com ativos que "
                "apoiam a sensação de leveza e conforto — complemento tópico da linha Flebogenol",
        "comp": "Creme com ativos vegetais para massagem nas pernas. Bisnaga 250ml.",
        "modo": "Aplicar nas pernas com movimentos ascendentes (dos tornozelos para as coxas), 1 a 2 vezes ao dia.",
        "faq": [
            ("Posso usar Fleboderm com Flebogenol comprimidos?",
             "Sim, o creme complementa por fora o cuidado que o Pinus pinaster faz por dentro."),
        ],
    },
    "Flebogenol 30": {
        "cat": "Circulação",
        "oque": "extrato seco de Pinus pinaster (picnogenol) 50mg em comprimidos (30 "
                "unidades) — antioxidante que apoia a microcirculação e o conforto das pernas",
        "comp": "Extrato seco de Pinus pinaster Aiton 50mg por comprimido. 30 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("Para que serve o Pinus pinaster?",
             "Os proantocianidinas da casca do pinheiro marítimo francês são antioxidantes estudados para a saúde da microcirculação e sensação de pernas leves."),
            ("Flebogenol serve para varizes?",
             "Ele apoia o conforto circulatório; para tratamento de varizes, consulte um angiologista."),
        ],
    },
    "Flebogenol 60": {
        "cat": "Circulação",
        "oque": "embalagem econômica (60 comprimidos) do extrato de Pinus pinaster "
                "50mg para uso contínuo no cuidado da microcirculação",
        "comp": "Extrato seco de Pinus pinaster Aiton 50mg por comprimido. 60 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, com água.",
        "faq": [
            ("Por quanto tempo usar Flebogenol?",
             "O uso contínuo por 60 a 90 dias é comum para perceber o benefício no conforto das pernas."),
        ],
    },
    "Flex-a-Mim": {
        "cat": "Articulações",
        "oque": "glucosamina 500mg + condroitina 400mg com metionina em comprimidos "
                "(60 unidades), dupla clássica que auxilia na manutenção da função articular — "
                "sem glúten e sem lactose",
        "comp": "Sulfato de glucosamina 500mg, sulfato de condroitina 400mg e metionina. 60 comprimidos.",
        "modo": "Tomar 1 comprimido 2 a 3 vezes ao dia, ou conforme orientação profissional.",
        "faq": [
            ("Glucosamina e condroitina funcionam?",
             "São os blocos construtores da cartilagem; estudos mostram apoio ao conforto articular com uso regular por 8 a 12 semanas."),
        ],
    },
    "Gargotoss": {
        "cat": "Respiratório e Garganta",
        "oque": "pastilhas para a garganta com vitaminas C, D e zinco (10 pastilhas "
                "de 1g), que perfumam o hálito e apoiam a imunidade",
        "comp": "Vitaminas C e D, zinco. 10 pastilhas de 1g.",
        "modo": "Dissolver 1 pastilha na boca até 3 vezes ao dia.",
        "faq": [
            ("Gargotoss serve para dor de garganta?",
             "As pastilhas acalmam e hidratam a garganta enquanto a vitamina C e o zinco apoiam as defesas naturais."),
        ],
    },
    "LacIntesty 10": {
        "cat": "Digestão e Fígado",
        "oque": "enzima lactase (Aspergillus oryzae) 10.000 U.FCC em comprimidos "
                "mastigáveis (10 unidades) que auxilia na digestão da lactose",
        "comp": "Lactase (Aspergillus oryzae) 10.000 U.FCC por comprimido. 10 comprimidos mastigáveis.",
        "modo": "Mastigar 1 comprimido imediatamente antes de consumir leite ou derivados.",
        "faq": [
            ("Como tomar lactase?",
             "Sempre junto (ou até 5 minutos antes) do alimento com lactose — o efeito vale só para aquela refeição."),
            ("Posso tomar lactase todos os dias?",
             "Sim, a enzima age apenas no alimento dentro do intestino e não causa dependência."),
        ],
    },
    "LacIntesty 30": {
        "cat": "Digestão e Fígado",
        "oque": "lactase 10.000 U.FCC em embalagem com 30 comprimidos mastigáveis "
                "para quem convive diariamente com a intolerância à lactose",
        "comp": "Lactase (Aspergillus oryzae) 10.000 U.FCC por comprimido. 30 comprimidos.",
        "modo": "Mastigar 1 comprimido imediatamente antes de consumir lactose.",
        "faq": [
            ("Qual dose de lactase escolher?",
             "10.000 U.FCC cobre refeições típicas com leite e queijos; refeições muito ricas em lactose podem pedir dose extra."),
        ],
    },
    "LacIntesty 60": {
        "cat": "Digestão e Fígado",
        "oque": "embalagem família da lactase LacIntesty 10.000 U.FCC — 60 "
                "comprimidos mastigáveis, o melhor custo por dose",
        "comp": "Lactase (Aspergillus oryzae) 10.000 U.FCC por comprimido. 60 comprimidos.",
        "modo": "Mastigar 1 comprimido imediatamente antes de consumir lactose.",
        "faq": [
            ("A lactase LacIntesty é vegana?",
             "A enzima é produzida por fermentação do fungo Aspergillus oryzae, sem origem animal."),
        ],
    },
    "Lactase 10": {
        "cat": "Digestão e Fígado",
        "oque": "enzima lactase 10.000 FCC em comprimidos (10 unidades), zero açúcar "
                "e sem glúten, para digerir leite e derivados sem desconforto",
        "comp": "Lactase 10.000 FCC por comprimido. 10 comprimidos.",
        "modo": "Tomar 1 comprimido imediatamente antes de alimentos com lactose.",
        "faq": [
            ("O que acontece se eu esquecer a lactase?",
             "Sem a enzima, a lactose fermenta no intestino causando gases, estufamento e diarreia em intolerantes."),
        ],
    },
    "Lactitol 120ml": {
        "cat": "Intestino e Fibras",
        "oque": "lactitol em solução oral (120ml) — laxante osmótico suave que "
                "auxilia o bom funcionamento do intestino, com sabor agradável",
        "comp": "Lactitol em solução oral. Frasco 120ml.",
        "modo": "Adultos: 1 a 2 colheres de sopa ao dia, de preferência à noite. Ajustar conforme resposta.",
        "faq": [
            ("Lactitol causa dependência intestinal?",
             "Não; por ser osmótico, ele atrai água para o bolo fecal sem irritar o intestino, sendo indicado para uso prolongado."),
        ],
    },
    "Lactitol 200ml": {
        "cat": "Intestino e Fibras",
        "oque": "lactitol em solução oral no frasco econômico de 200ml, regulador "
                "intestinal osmótico de ação suave",
        "comp": "Lactitol em solução oral. Frasco 200ml.",
        "modo": "Adultos: 1 a 2 colheres de sopa ao dia, de preferência à noite.",
        "faq": [
            ("Em quanto tempo o lactitol age?",
             "O efeito costuma ocorrer em 24 a 48 horas de uso regular."),
        ],
    },
    "Lactulose": {
        "cat": "Intestino e Fibras",
        "oque": "lactulose 666mg/ml em solução oral (120ml) — clássico regulador "
                "osmótico do trânsito intestinal, uso adulto",
        "comp": "Lactulose 666mg/ml. Frasco 120ml.",
        "modo": "Adultos: 15 a 30ml ao dia, preferencialmente após o café da manhã.",
        "faq": [
            ("Qual a diferença entre lactulose e lactitol?",
             "Ambos são osmóticos; a lactulose é o padrão clássico, o lactitol tem sabor mais neutro e costuma dar menos gases."),
        ],
    },
    "Laxtrine Fibras": {
        "cat": "Intestino e Fibras",
        "oque": "mix de fibras em pó sem sabor (250g): polidextrose, inulina, FOS, "
                "ameixa e pectina — fibras prebióticas que auxiliam o funcionamento do intestino",
        "comp": "Polidextrose, frutooligossacarídeos (FOS), inulina, ameixa em pó, pectina. Pote 250g, sem açúcar e sem glúten.",
        "modo": "Misturar 1 colher de sopa em água, suco ou iogurte, 1 a 2 vezes ao dia. Beba bastante água.",
        "faq": [
            ("Fibras prebióticas fazem o quê?",
             "Alimentam as bactérias boas do intestino (efeito prebiótico) e dão volume ao bolo fecal, regulando o trânsito."),
            ("Posso misturar no café ou na comida?",
             "Sim, o mix é neutro e não altera o sabor de bebidas e preparações."),
        ],
    },
    "Laxtrine Geleia": {
        "cat": "Intestino e Fibras",
        "oque": "geleia de fibras (250g) com tamarindo, ameixa, cacau, inulina, FOS, "
                "polidextrose e pectina — jeito gostoso de regular o intestino, sem açúcar e sem glúten",
        "comp": "Tamarindo, ameixa, cacau, inulina, FOS, polidextrose e pectina. Pote 250g.",
        "modo": "Tomar 1 colher de sopa ao dia, pura ou com pão/torradas, de preferência à noite.",
        "faq": [
            ("Criança pode comer Laxtrine Geleia?",
             "Consulte o pediatra para a dose adequada; a base de frutas e fibras é bem tolerada."),
        ],
    },
    "Meltrat Pastilha": {
        "cat": "Respiratório e Garganta",
        "oque": "pastilhas diet de mel com própolis (caixa com 12 latinhas de 30g) "
                "que perfumam o hálito e aliviam naturalmente a garganta, sem açúcar",
        "comp": "Mel, própolis e eucalipto. Pastilhas diet sem açúcar. 12 latas de 30g.",
        "modo": "Dissolver 1 pastilha na boca sempre que precisar de alívio para a garganta.",
        "faq": [
            ("Própolis ajuda a garganta?",
             "Sim, a própolis tem propriedades que acalmam a irritação e apoiam as defesas naturais da mucosa."),
        ],
    },
    "Meltrat Spray": {
        "cat": "Respiratório e Garganta",
        "oque": "spray de mel com própolis e gengibre (30ml) — alívio direto e "
                "imediato para a garganta irritada, prático para levar sempre",
        "comp": "Mel, própolis e gengibre em solução spray. Frasco 30ml.",
        "modo": "Aplicar 2 a 3 jatos diretamente na garganta, até 4 vezes ao dia.",
        "faq": [
            ("Quando usar o spray em vez da pastilha?",
             "O spray atinge diretamente a mucosa para alívio imediato; a pastilha prolonga o contato dos ativos."),
        ],
    },
    "Meltrat Xarope": {
        "cat": "Respiratório e Garganta",
        "oque": "xarope de mel com guaco e agrião (120ml), fonte de vitamina C — "
                "receita tradicional brasileira para o conforto respiratório, uso adulto e pediátrico",
        "comp": "Mel, guaco, agrião e vitamina C. Frasco 120ml.",
        "modo": "Adultos: 1 colher de sopa 3 vezes ao dia. Crianças: 1 colher de chá 3 vezes ao dia, ou conforme o pediatra.",
        "faq": [
            ("Guaco serve para quê?",
             "O guaco é tradicionalmente usado como expectorante natural, ajudando a soltar o catarro."),
        ],
    },
    "Metilcobalamina": {
        "cat": "Linha Inovitann",
        "oque": "vitamina B12 na forma ativa (metilcobalamina) da linha Inovitann "
                "Clinical — 414% da IDR em comprimidos mastigáveis, sem açúcar, glúten ou lactose "
                "(60 comprimidos)",
        "comp": "Metilcobalamina (B12 ativa) — 414% da IDR. 60 comprimidos mastigáveis 1x ao dia.",
        "modo": "Mastigar 1 comprimido ao dia.",
        "faq": [
            ("B12 dá energia?",
             "A B12 participa da formação das células vermelhas e do metabolismo energético; corrigir a deficiência combate cansaço e formigamentos."),
        ],
    },
    "MForce": {
        "cat": "Ossos e Músculos",
        "oque": "HMB (hidroximetilbutirato de cálcio) 800mg em comprimidos (90 "
                "unidades) — metabólito da leucina que apoia a força e a preservação da massa "
                "muscular, sem açúcar e sem glúten",
        "comp": "Hidroximetilbutirato de cálcio (HMB) 800mg por comprimido. 90 comprimidos.",
        "modo": "Tomar 3 comprimidos ao dia (2,4g de HMB), divididos nas refeições.",
        "faq": [
            ("Para que serve o HMB?",
             "O HMB reduz a degradação de proteína muscular, apoiando força e recuperação — útil em treinos intensos e na prevenção da sarcopenia em 60+."),
        ],
    },
    "Mucolisil 20mg": {
        "cat": "Respiratório e Garganta",
        "oque": "acetilcisteína 20mg/ml em solução oral sabor framboesa (120ml), "
                "que fluidifica o catarro — dosagem pediátrica/suave, sem açúcar",
        "comp": "Acetilcisteína (NAC) 20mg/ml, sabor framboesa. Frasco 120ml.",
        "modo": "Uso oral conforme orientação, em geral 3 doses ao dia. Beber bastante água potencializa o efeito.",
        "faq": [
            ("Como a acetilcisteína age no catarro?",
             "Ela quebra as ligações do muco, deixando-o mais fluido e fácil de eliminar."),
        ],
    },
    "Mucolisil 40mg": {
        "cat": "Respiratório e Garganta",
        "oque": "acetilcisteína 40mg/ml em solução oral sabor framboesa (120ml) — "
                "dosagem adulto para fluidificar secreções das vias respiratórias",
        "comp": "Acetilcisteína (NAC) 40mg/ml, sabor framboesa. Frasco 120ml.",
        "modo": "Uso adulto: conforme orientação, em geral 15ml até 3 vezes ao dia.",
        "faq": [
            ("Mucolisil serve para tosse seca ou com catarro?",
             "Para tosse produtiva (com catarro): ele fluidifica a secreção para facilitar a eliminação."),
        ],
    },
    "Muricalm BabyColli": {
        "cat": "Infantil",
        "oque": "suspensão oral infantil (60ml com seringa dosadora) de sabor "
                "agradável, suave e segura para o conforto dos bebês com cólicas",
        "comp": "Extratos vegetais calmantes suaves. Frasco 60ml + seringa dosadora. Sem açúcar.",
        "modo": "Uso pediátrico: dosagem conforme peso/idade, sob orientação do pediatra.",
        "faq": [
            ("A partir de quando o bebê pode usar?",
             "Consulte o pediatra; a fórmula foi desenvolvida para ser suave e segura nos primeiros meses."),
        ],
    },
    "Muricalm Comprimidos": {
        "cat": "Sono e Cognição",
        "oque": "composto de maracujá em comprimidos mastigáveis (30 unidades) — "
                "calmante natural de rápida absorção para momentos de tensão e para relaxar antes de dormir",
        "comp": "Composto de Passiflora incarnata (maracujá) e ervas calmantes. 30 comprimidos mastigáveis.",
        "modo": "Mastigar 1 comprimido até 3 vezes ao dia ou 30 minutos antes de dormir.",
        "faq": [
            ("Maracujá dá sono?",
             "A passiflora tem efeito ansiolítico suave que favorece o relaxamento e a qualidade do sono, sem causar sedação forte."),
        ],
    },
    "Muricalm Gotas": {
        "cat": "Sono e Cognição",
        "oque": "calmante natural em gotas (30ml, 600 doses) de rápida absorção, com "
                "melatonina — para a rotina do sono e momentos de agitação",
        "comp": "Extratos calmantes e melatonina em gotas. Frasco 30ml (600 doses).",
        "modo": "Tomar as gotas recomendadas 30 minutos antes de dormir, puras ou em água.",
        "faq": [
            ("Melatonina precisa de receita?",
             "No Brasil, a melatonina em doses de suplemento (até 0,21mg) é liberada para maiores de 19 anos sem receita."),
        ],
    },
    "NAC": {
        "cat": "Linha Inovitann",
        "oque": "NAC Ultra da linha Inovitann Clinical: N-acetil L-cisteína 600mg em "
                "cápsulas (60 unidades) — precursora da glutationa, o antioxidante mestre do "
                "organismo; sem açúcar, glúten ou lactose",
        "comp": "N-acetil L-cisteína 600mg por cápsula. 60 cápsulas.",
        "modo": "Tomar 1 cápsula ao dia, de preferência longe das refeições.",
        "faq": [
            ("Para que serve o NAC?",
             "O NAC repõe cisteína para a síntese de glutationa, apoiando o sistema antioxidante, o fígado e a saúde respiratória."),
            ("NAC 600mg é dose segura?",
             "600mg/dia é a dose clássica usada em estudos, bem tolerada em adultos saudáveis."),
        ],
    },
    "NoGlute": {
        "cat": "Digestão e Fígado",
        "oque": "protease de Aspergillus niger (585.000 PPI) em cápsulas — enzima "
                "que pode auxiliar na digestão do glúten, para desconfortos de sensibilidade "
                "não celíaca; sem açúcar",
        "comp": "Protease específica de Aspergillus niger 585.000 PPI por cápsula.",
        "modo": "Tomar 1 cápsula imediatamente antes de refeições com glúten.",
        "faq": [
            ("NoGlute serve para celíacos?",
             "Não — celíacos devem manter dieta 100% sem glúten. O NoGlute apoia quem tem sensibilidade não celíaca em exposições eventuais."),
        ],
    },
    "Orapronobis": {
        "cat": "Compostos Naturais",
        "oque": "ora-pro-nóbis em cápsulas (60 unidades) da Santa Raiz — a folha "
                "proteica da tradição mineira, rica em proteínas, fibras, ferro e vitaminas",
        "comp": "Folha de ora-pro-nóbis (Pereskia aculeata) desidratada. 60 cápsulas.",
        "modo": "Tomar 2 cápsulas ao dia, com água.",
        "faq": [
            ("Ora-pro-nóbis é rica em quê?",
             "É conhecida como 'carne de pobre': até 25% de proteína na folha seca, além de fibras, ferro, cálcio e vitaminas A e C."),
        ],
    },
    "Osteocorp 500mg": {
        "cat": "Ossos e Músculos",
        "oque": "cálcio elementar 500mg por comprimido (60 unidades) — dose plena "
                "de cálcio para ossos e dentes, zero açúcar",
        "comp": "Cálcio elementar 500mg por comprimido. 60 comprimidos.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Qual o melhor horário para tomar cálcio?",
             "Junto às refeições, e de preferência longe de suplementos de ferro, que competem pela absorção."),
        ],
    },
    "Osteocorp MDK": {
        "cat": "Ossos e Músculos",
        "oque": "fórmula óssea completa: cálcio + magnésio + zinco + vitaminas D3 e "
                "K (60 comprimidos) — o cálcio no lugar certo, com os cofatores que fixam o "
                "mineral nos ossos",
        "comp": "Cálcio, magnésio, zinco, vitamina D3 e vitamina K. 60 comprimidos, zero açúcar.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Por que cálcio com vitaminas D e K?",
             "A vitamina D aumenta a absorção intestinal do cálcio e a K2 direciona o mineral para os ossos, e não para as artérias."),
        ],
    },
    "Paracetamol 30": {
        "cat": "Dor e Febre",
        "oque": "paracetamol 750mg com 30 comprimidos — analgésico e antitérmico "
                "para alívio de dores e febre, uso adulto",
        "comp": "Paracetamol 750mg por comprimido. 30 comprimidos.",
        "modo": "Adultos: 1 comprimido a cada 6 horas, se necessário. Não exceder 4 comprimidos ao dia.",
        "faq": [
            ("Qual o intervalo seguro do paracetamol 750mg?",
             "Mínimo de 4 a 6 horas entre doses, máximo de 3g/dia (4 comprimidos) para adultos saudáveis."),
        ],
    },
    "Paracetamol 200": {
        "cat": "Dor e Febre",
        "oque": "paracetamol 750mg em embalagem hospitalar/família com 200 "
                "comprimidos — analgésico e antitérmico, uso adulto",
        "comp": "Paracetamol 750mg por comprimido. 200 comprimidos.",
        "modo": "Adultos: 1 comprimido a cada 6 horas, se necessário. Máximo 4 ao dia.",
        "faq": [
            ("Paracetamol pode com álcool?",
             "Evite: a combinação sobrecarrega o fígado. Em uso frequente de álcool, consulte um médico antes."),
        ],
    },
    "Protobaby": {
        "cat": "Infantil",
        "oque": "suplemento infantil em suspensão (30ml) com vitaminas A, C e D, "
                "ácido fólico, ferro e zinco — os micronutrientes-chave dos primeiros anos",
        "comp": "Vitaminas A, C e D, ácido fólico, ferro e zinco. Frasco 30ml com conta-gotas.",
        "modo": "Uso pediátrico: gotas conforme orientação do pediatra.",
        "faq": [
            ("Por que bebês suplementam ferro e vitamina D?",
             "A Sociedade Brasileira de Pediatria recomenda vitamina D desde o nascimento e ferro a partir dos 6 meses (ou antes, em prematuros)."),
        ],
    },
    "Q10": {
        "cat": "Linha Inovitann",
        "oque": "Coenzima Q10 Plus 100mg da linha Inovitann Clinical (60 cápsulas) — "
                "o combustível das mitocôndrias, para energia celular e saúde cardiovascular; "
                "sem açúcar, glúten ou lactose",
        "comp": "Coenzima Q10 (ubiquinona) 100mg por cápsula. 60 cápsulas.",
        "modo": "Tomar 1 cápsula ao dia, junto a uma refeição com gordura (melhora a absorção).",
        "faq": [
            ("Quem usa estatina deve tomar Q10?",
             "Estatinas reduzem a produção natural de CoQ10; muitos médicos recomendam a reposição para minimizar dores musculares."),
            ("Q10 serve para o coração?",
             "A CoQ10 concentra-se nos tecidos de alta demanda energética, como o músculo cardíaco, apoiando sua função."),
        ],
    },
    "Reporgermina": {
        "cat": "Intestino e Fibras",
        "oque": "probiótico Saccharomyces cerevisiae (500.000.000 UFC/10ml) em 5 "
                "flaconetes — reforço da flora intestinal em episódios de desequilíbrio, uso adulto",
        "comp": "Saccharomyces cerevisiae 500 milhões UFC por flaconete de 10ml. 5 flaconetes.",
        "modo": "Agitar e tomar 1 flaconete ao dia, puro ou diluído.",
        "faq": [
            ("Quando usar probióticos?",
             "Após antibióticos, em episódios de diarreia ou desequilíbrio intestinal, para repovoar a flora com microrganismos benéficos."),
        ],
    },
    "Reporgermina Ped": {
        "cat": "Infantil",
        "oque": "versão pediátrica do probiótico Saccharomyces cerevisiae em "
                "suspensão oral (5 flaconetes) para a flora intestinal das crianças",
        "comp": "Saccharomyces cerevisiae 250 milhões UFC por flaconete. 5 flaconetes pediátricos.",
        "modo": "Uso pediátrico: 1 flaconete ao dia, conforme orientação do pediatra.",
        "faq": [
            ("Probiótico ajuda criança com diarreia?",
             "Sim, probióticos encurtam episódios de diarreia aguda e apoiam a recuperação da flora infantil."),
        ],
    },
    "Sulfato Ferroso 60": {
        "cat": "Ferro e Anemia",
        "oque": "sulfato ferroso em comprimidos (60 unidades) — a forma clássica e "
                "acessível de reposição de ferro, zero açúcar e sem glúten",
        "comp": "Sulfato ferroso. 60 comprimidos revestidos.",
        "modo": "Tomar 1 comprimido ao dia, de estômago vazio ou com suco cítrico, longe de leite e café.",
        "faq": [
            ("Sulfato ferroso escurece as fezes?",
             "Sim, é um efeito esperado e inofensivo da suplementação de ferro."),
        ],
    },
    "Valfresh": {
        "cat": "Respiratório e Garganta",
        "oque": "pastilhas diet sabor menta (12 latinhas de 30g) que perfumam o "
                "hálito e acalmam a garganta, sem açúcar",
        "comp": "Pastilhas de menta diet, sem açúcar. 12 latas de 30g.",
        "modo": "Dissolver 1 pastilha na boca sempre que quiser refrescar o hálito.",
        "faq": [
            ("Valfresh tem açúcar?",
             "Não, é uma pastilha diet — refresca sem contribuir para cáries ou picos de glicose."),
        ],
    },
    "Cúrcuma": {
        "cat": "Linha Inovitann",
        "oque": "Cúrcuma Plus da linha Inovitann Clinical (60 cápsulas) — extrato de "
                "Curcuma longa padronizado em curcuminoides, o antioxidante e "
                "anti-inflamatório natural mais estudado do mundo",
        "comp": "Extrato seco de Curcuma longa padronizado em curcuminoides. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, junto a uma refeição com gordura ou pimenta-do-reino (melhora a absorção).",
        "faq": [
            ("Para que serve a curcumina?",
             "A curcumina modula vias inflamatórias e oxidativas, apoiando articulações, fígado e recuperação muscular."),
        ],
    },
    "LUT+ZEA": {
        "cat": "Linha Inovitann",
        "oque": "Luteína + Zeaxantina da linha Inovitann Clinical (60 cápsulas) — "
                "os carotenoides que formam o pigmento macular, protegendo os olhos da luz "
                "azul de telas e do envelhecimento visual",
        "comp": "Luteína e zeaxantina de fontes naturais. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, junto a uma refeição com gordura.",
        "faq": [
            ("Luteína protege da luz azul?",
             "Sim, luteína e zeaxantina se concentram na mácula e filtram a luz azul, funcionando como 'óculos de sol internos'."),
        ],
    },
    "Magnésio L-Treonina": {
        "cat": "Linha Inovitann",
        "oque": "Magnésio L-Treonato da linha Inovitann Clinical (60 cápsulas) — a "
                "única forma de magnésio estudada por atravessar a barreira "
                "hematoencefálica, apoiando memória, foco e qualidade do sono",
        "comp": "Magnésio L-treonato (Magtein®-like). 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula à noite, cerca de 1 hora antes de dormir.",
        "faq": [
            ("Qual a diferença do L-treonato para outros magnésios?",
             "O L-treonato eleva o magnésio no cérebro, sendo a forma preferida para foco, memória e sono — não para reposição muscular."),
        ],
    },
    "Penta Magnésio": {
        "cat": "Linha Inovitann",
        "oque": "Penta Magnésio da linha Inovitann Clinical (60 cápsulas) — 5 formas "
                "de magnésio em uma única cápsula (bisglicinato, malato, taurato, citrato e "
                "óxido) para cobertura completa: músculos, energia, coração e mente",
        "comp": "Magnésio bisglicinato, malato, taurato, citrato e óxido. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, de preferência à noite.",
        "faq": [
            ("Por que 5 formas de magnésio?",
             "Cada forma tem absorção e afinidade tecidual diferentes; a combinação garante biodisponibilidade ampla no organismo."),
        ],
    },
    "Trimagnésio": {
        "cat": "Linha Inovitann",
        "oque": "Trimagnésio Ultra da linha Inovitann Clinical (60 cápsulas) — três "
                "formas de alta absorção (bisglicinato, malato e taurato) para músculos, "
                "energia e coração, sem os efeitos laxativos do óxido",
        "comp": "Magnésio bisglicinato, malato e taurato. 60 cápsulas. Sem açúcar, glúten ou lactose.",
        "modo": "Tomar 1 cápsula ao dia, de preferência à noite.",
        "faq": [
            ("Trimagnésio solta o intestino?",
             "As formas queladas (bisglicinato, malato, taurato) são bem absorvidas e raramente causam efeito laxativo."),
        ],
    },
    "Muricalm Xarope": {
        "cat": "Sono e Cognição",
        "oque": "composto calmante de maracujá em xarope — a versão líquida do "
                "Muricalm para relaxar e favorecer um sono tranquilo",
        "comp": "Composto de Passiflora incarnata (maracujá) e ervas calmantes em xarope.",
        "modo": "Tomar 1 colher de sopa (15ml) até 3 vezes ao dia ou antes de dormir.",
        "faq": [
            ("Xarope ou comprimido de maracujá?",
             "O efeito é o mesmo; o xarope agrada quem tem dificuldade com comprimidos e permite ajuste fino da dose."),
        ],
    },
    "Osteocorp 500 + 400": {
        "cat": "Ossos e Músculos",
        "oque": "cálcio 500mg + vitamina D3 400UI por comprimido — a dupla clássica "
                "para absorção e fixação do cálcio nos ossos",
        "comp": "Cálcio elementar 500mg e vitamina D3 400UI por comprimido.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Por que cálcio com vitamina D?",
             "Sem vitamina D, o intestino absorve pouco cálcio; a D3 400UI garante o aproveitamento do mineral."),
        ],
    },
    "Osteocorp 600 + 400": {
        "cat": "Ossos e Músculos",
        "oque": "cálcio 600mg + vitamina D3 400UI por comprimido — dose reforçada "
                "de cálcio para a saúde óssea, com a vitamina D que garante a absorção",
        "comp": "Cálcio elementar 600mg e vitamina D3 400UI por comprimido.",
        "modo": "Tomar 1 comprimido ao dia, junto a uma refeição.",
        "faq": [
            ("Qual Osteocorp escolher?",
             "500+400 para complementar uma dieta razoável em laticínios; 600+400 quando a ingestão alimentar de cálcio é baixa."),
        ],
    },
    "Vitônico": {
        "cat": "Vitaminas",
        "oque": "tônico vitamínico completo com vitaminas e minerais essenciais "
                "para energia, disposição e recuperação do apetite",
        "comp": "Polivitamínico e minerais em solução oral.",
        "modo": "Tomar 1 colher de sopa (15ml) ao dia, junto a uma refeição.",
        "faq": [
            ("Para quem é indicado um tônico vitamínico?",
             "Para períodos de cansaço, convalescença ou baixa ingestão alimentar, repondo micronutrientes essenciais."),
        ],
    },
    "Vitamina K": {
        "cat": "Linha Inovitann",
        "oque": "Vitamina K Ultra 146,06mcg da linha Inovitann Clinical (60 "
                "cápsulas, 1x ao dia) — essencial para a coagulação normal e a fixação do "
                "cálcio nos ossos; sem açúcar, glúten ou lactose",
        "comp": "Vitamina K 146,06mcg por cápsula. 60 cápsulas.",
        "modo": "Tomar 1 cápsula ao dia, junto a uma refeição com gordura.",
        "faq": [
            ("Vitamina K serve para os ossos?",
             "Sim, ela ativa a osteocalcina, proteína que fixa o cálcio na matriz óssea."),
            ("Quem toma anticoagulante pode usar vitamina K?",
             "Usuários de varfarina devem consultar o médico antes, pois a vitamina K interfere no efeito do medicamento."),
        ],
    },
}
