from program import program

if __name__ == '__main__':
    program = program.Program()
    while program.running:
        program.update()
    program.end()