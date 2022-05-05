mkdir datasets
cd datasets || exit 1
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_01_easy/MH_01_easy.zip
tar -xzf MH_01_easy.zip
rm MH_01_easy.zip
cd ..

virtualenv -p python3.8 venv
# shellcheck source=/dev/null
source venv/bin/activate
pip install -r requirements.txt
deactivate
