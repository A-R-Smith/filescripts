#! /bin/bash
sudo azcopy \
        --source https://nwford.file.core.windows.net/ford/prod/ \
        --destination https://nwford.file.core.windows.net/fordbck/ \
        --source-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbO$
        --dest-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqg$
        --recursive \
        --exclude-older --exclude-newer
sudo azcopy \
        --source https://nwford.file.core.windows.net/ford/prod/ \
        --destination https://nwford.blob.core.windows.net/nwfordhd-2017-08-28t$
        --source-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbO$
        --dest-key QJyO9oM3YVahmJ1zKkEPEABTq3W5MMWYGOoyRHDoFdb42FSVVInawPmJbOqg$
        --recursive \
        --exclude-older --exclude-newer
