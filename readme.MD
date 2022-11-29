### Short Description
This script is used to capture thermal and rgb images simultaneously alongside with the ground truth (respiratory rate signal and ECG signal)

Further explanation will be added soon. Current readme is for my own reference.

### Run Example
```bash
python run_capture.py --name martin60d --cdown 15 --duration 60 --devicethermal 0 --devicergb 2 --dps 20 --conn usb
```

```bash
python verify_data.py --subject martin60c
```

```bash
python do_backup.py --subject=deletemepls2 --saveloc=D:
```