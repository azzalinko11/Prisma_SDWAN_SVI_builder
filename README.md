Work in progress

1 Update the CSV with the values you require<br>
2 Updated the crendetails_file.py.example with your tenant API details then rename to crendetails_file.py<br>
3 run Python3 svi_creator.py<br>

Inital testing on 1200-S
<br>
Replace the site_id & Element ID with your ID's
    try:
        response = sdk.post.interfaces(
            site_id='1705604220721000796',
            element_id='1705534739582007296',
            data=svi_data_json,
            api_version="v4.17"
