import lexer

while True:
    text = input("anaconda >")
    result, error = lexer.run("<ACSHELL>", text)

    if error:
        print(error)
    else:
        print(result)
