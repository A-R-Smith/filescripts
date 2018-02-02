#! /bin/bash
sudo azcopy \
        --source https://nwford.file.core.windows.net/ford/prod/ \
        --destination https://nwford.file.core.windows.net/fordbck/ \
        --source-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqgO+/vVCu5Rxdjj2ka4+dO7DlHbw== \
        --dest-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqgO+/vVCu5Rxdjj2ka4+dO7DlHbw== \
        --recursive \
        --exclude-older --exclude-newer
sudo azcopy \
        --source https://nwford.file.core.windows.net/ford/prod/ \
        --destination https://nwford.blob.core.windows.net/nwfordhd-2017-08-28t14-42-20-095z/ford/ \
        --source-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqgO+/vVCu5Rxdjj2ka4+dO7DlHbw== \
        --dest-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqgO+/vVCu5Rxdjj2ka4+dO7DlHbw== \
        --recursive \
        --exclude-older --exclude-newer
