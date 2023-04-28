if (($# < 1)); then
	echo "USAGE: init.sh <museumName>"
	exit 1
fi
museum=$1
DIR="./data/$museum"

if [ -d "$DIR" ]; then

	if [ -f "$DIR/artworks.json" ]; then
		cp ./data/$museum/artworks.json ../cmServer/cmSpice/data/artworks.json
	fi
	cp ./data/$museum/seedFile.json ../cmServer/cmSpice/data/seedFile.json
	cp ./data/$museum/seedFile.json ../apiServer/app/src/seedFile.json
	cp ./data/$museum/network.yml ../deploy/network.yml
	cp ./data/$museum/template.env ../deploy/.env
else
	echo "data folder not found for $museum"
fi

pushd ../deploy
docker-compose --env-file .env build && docker-compose up
popd