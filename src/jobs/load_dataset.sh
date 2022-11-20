DATA_FOLDER=./dataset/nhnet
run_date=$1
echo "Start collecting news"
news-please -c $DATA_FOLDER/base/news_please
echo "News collected"
echo "Constructing new dataset"
python src/jobs/collect_NewSHead_dataset.py $DATA_FOLDER $run_date --dataset-files train.json valid.json test.json
echo "Dataset constructed"
echo "Removing trash"
rm -r /tmp/nhnet
rm -r ./news-please-repo
#mv ./tmp/nhnet $DATA_FOLDER/$run_date/parsed