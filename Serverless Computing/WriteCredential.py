# Update the path below.
file = 'C:/Users/Fuen/.aws/credentials'

# Update keys below.
AWS_ACCESS_KEY_ID = 'AKIA2N6AFDGLP3XBJ6EF'
AWS_SECRET_KEY = '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'

with open(file, 'w') as filetowrite:
    myCredential = f"""[default]
aws_access_key_id={AWS_ACCESS_KEY_ID}
aws_secret_access_key={AWS_SECRET_KEY}
"""
    filetowrite.write(myCredential)

# Update the path below.
file = 'C:/Users/Fuen/.aws/config'

with open(file, 'w') as filetowrite:
    myCredential = """[default]
                      region = us-east-1
                      output = json
                      [profile prod]
                      region = us-east-1
                      output = json"""
    filetowrite.write(myCredential)
