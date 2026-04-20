import wget

base_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/"
extension = ".png"

for i in range(1, 906):
	url = base_url + '{0:03}'.format(i) + extension
	filename = wget.download(url, "app/static/img/pokemons/")


# url for pokemon data in readable format: https://gitlab.com/gguibon/uspn-storage/-/raw/main/pokemons.json
