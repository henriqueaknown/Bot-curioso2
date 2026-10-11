
from token import token
import discord
from discord.ext import commands
import requests
import pyttsx3
import random
import asyncio

# =========================
# INICIALIZAÇÃO
# =========================

engine = pyttsx3.init()

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default()
)

bot.intents.message_content = True

voz_atual = None

temas = {
    "ciencia": "ciência",
    "historia": "história",
    "astronomia": "astronomia",
    "geral": "conhecimento geral"
}


# =========================
# CONFIGURAÇÃO DE VOZ
# =========================

def listar_vozes():
    vozes = engine.getProperty("voices")

    for i, voz in enumerate(vozes):
        print(i, voz.name, voz.id)


def configurar_voz(tipo):
    global voz_atual

    vozes = engine.getProperty("voices")

    palavras = {
        "masculina": ["male", "homem", "masculino"],
        "feminina": ["female", "mulher", "feminino"]
    }

    for voz in vozes:
        nome = voz.name.lower()
        identificador = voz.id.lower()

        if any(p in nome or p in identificador
               for p in palavras[tipo]):
            engine.setProperty("voice", voz.id)
            voz_atual = tipo
            return True

    return False


def speak(texto):
    engine.say(texto)
    engine.runAndWait()


# =========================
# BUSCAR FATOS NA WIKIPÉDIA
# =========================

def get_fact(tema):
    url = "https://pt.wikipedia.org/w/api.php"

    parametros = {
        "action": "query",
        "list": "search",
        "srsearch": temas[tema],
        "srlimit": 20,
        "format": "json"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=10,
            headers={"User-Agent": "DiscordFactBot/1.0"}
        )

        if resposta.status_code != 200:
            return None, None

        dados = resposta.json()
        resultados = dados["query"]["search"]

        if not resultados:
            return None, None

        artigo = random.choice(resultados)
        titulo = artigo["title"]

        parametros_artigo = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": titulo,
            "format": "json"
        }

        resposta_artigo = requests.get(
            url,
            params=parametros_artigo,
            timeout=10,
            headers={"User-Agent": "DiscordFactBot/1.0"}
        )

        if resposta_artigo.status_code != 200:
            return None, None

        paginas = resposta_artigo.json()["query"]["pages"]
        pagina = next(iter(paginas.values()))
        resumo = pagina.get("extract", "").strip()

        if not resumo:
            return None, None

        link = (
            "https://pt.wikipedia.org/wiki/"
            + requests.utils.quote(titulo.replace(" ", "_"))
        )

        return resumo[:1200], link

    except (requests.RequestException, ValueError, KeyError):
        return None, None


# =========================
# BOAS-VINDAS
# =========================

@bot.command()
async def start(ctx):
    await ctx.send(
        f"Olá, {ctx.author.name}! "
        "Use !fact para descobrir uma curiosidade."
    )


# =========================
# CURIOSIDADES POR TEMA
# =========================

@bot.command()
async def fact(ctx, tema="geral"):
    tema = tema.lower()

    if tema not in temas:
        await ctx.send(
            "Tema inválido! Escolha: ciencia, historia, "
            "astronomia ou geral."
        )
        return

    await ctx.send(
        f"🔎 Pesquisando sobre {temas[tema]}..."
    )

    curiosidade, link = await asyncio.to_thread(
        get_fact, tema
    )

    if curiosidade is None:
        await ctx.send(
            "Não foi possível obter a curiosidade. "
            "Tente novamente mais tarde."
        )
        return

    mensagem = (
        f"📚 **Tema: {temas[tema].title()}**\n"
        f"{curiosidade}\n\n"
        f"Fonte para consulta: {link}"
    )

    await ctx.send(mensagem)

    # A fala é executada em uma thread separada
    await asyncio.to_thread(speak, curiosidade)


# =========================
# ESCOLHER VOZ
# =========================

@bot.command()
async def voz(ctx, tipo=None):
    if tipo is None:
        await ctx.send(
            "Use !voz masculina ou !voz feminina."
        )
        return

    tipo = tipo.lower()

    if tipo not in ["masculina", "feminina"]:
        await ctx.send(
            "Opção inválida! Escolha masculina ou feminina."
        )
        return

    sucesso = configurar_voz(tipo)

    if sucesso:
        await ctx.send(
            f"Configuração de voz alterada para {tipo}."
        )
    else:
        await ctx.send(
            f"Não encontrei uma voz identificada como "
            f"{tipo} neste computador. Consulte as vozes "
            "disponíveis no terminal."
        )


# =========================
# LISTAR VOZES DISPONÍVEIS
# =========================

@bot.command()
async def vozes(ctx):
    vozes_disponiveis = engine.getProperty("voices")

    if not vozes_disponiveis:
        await ctx.send("Nenhuma voz foi encontrada.")
        return

    lista = "\n".join(
        f"{i + 1}. {v.name}"
        for i, v in enumerate(vozes_disponiveis)
    )

    await ctx.send(
        f"**Vozes instaladas neste computador:**\n{lista}"
    )


# =========================
# EXECUTAR O BOT
# =========================

bot.run()
