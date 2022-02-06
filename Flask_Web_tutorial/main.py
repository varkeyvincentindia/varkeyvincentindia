from website import create_app #Since website is a python package

app = create_app()

if __name__ =='__main__':
    app.run(debug=True) # debug=True means restart the webserver whenever changes 
    #are made to the code. Will be set to 'false' when app is in prodution 
