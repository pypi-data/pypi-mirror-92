class StringQualify:
    def format_token(self, token) -> str:
        str_return = token
        index = 0

        index = token.find('\"', index)
        while index > -1:
            if index != len(token)-1 and token[index+1] != '\"':
                index += 1
                str_return = self.insert_char(str_return, index, '\"')
            if index == len(token)-1:
                str_return = self.insert_char(str_return, index+1, '\"')
                index += 1
            index = token.find('\"', index)

        token = str_return
        index = token.find('\'', 0)
        while index > -1:
            if index == 0 and token[1] != '\'':
                str_return = self.insert_char(str_return, 1, '\'')
                str_return = self.insert_char(str_return, len(str_return), '\'')
            index += 1
            index = token.find('\'', index)
        return str_return

    def format_param(self, str_param) -> str:
        token = ""
        str_return = []
        i_token = 0
        tokens = str_param.split()

        i = 0
        while i < len(tokens):
            stoken = []
            token = tokens[i]
            if i_token > 0:
                str_return.append(" ")

            stoken.append(token)

            if token.startswith("\"") and not token.endswith("\""):
                for j in range(i+1, len(tokens)):
                    stoken.append(" ")
                    token = tokens[j]
                    stoken.append(token)

                    if token.find('\"') > -1:
                        i = j
                        break

            str_return.append(self.format_token(''.join(stoken)))
            i_token += 1
            i += 1

        str_return.insert(0, " \"")
        str_return.append('\"')
        return ''.join(str_return)

    def insert_char(self, string, index, char) -> str:
        return string[:index] + char + string[index:]
