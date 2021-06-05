import pandas
import telebot

class KivanoBot:
    __data = pandas.read_csv('internet_shop.csv')
    categories = set(__data.Group.to_list())
    names_of_products = __data.Name.to_list()


    def show_categories(self,args):
        if len(args) <= 0:
            return '\n'.join(self.categories)

        else:
            if args not in self.categories:
                return f'Категории с названием: {args} не существует'
            else:
                cat = self.__data[self.__data.Group == args]
                data = cat[['Name', 'Product price']].to_string()
                return data
    
    def show_product(self,arg):
        if '\r\n'+arg+'\r\n' not in self.names_of_products:
            return f'Товара с названием: {arg} не существует'
        else:
            #self.names_of_products = [item.replace('\r\n') for item in self.names_of_products]
            name = self.__data[self.__data.Name == '\r\n'+arg+'\r\n']
            data = name[['Name','Group','Product price']].to_string()
            return data


TOKEN = '1696669545:AAHyTcthV82miNaBvaw0lqAHZmJ2hwKIMWA'
bot = telebot.TeleBot(TOKEN)
kbot= KivanoBot()

@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)


@bot.message_handler(commands=['categories'])
def show_categories(message):
    args = message.text[12:]
    r = kbot.show_categories(args)
    if len(r) > 4096:
        for x in range(0, len(r), 4096):
            bot.send_message(message.chat.id, r[x:x + 4096])
    else:
        bot.send_message(message.chat.id, r)



@bot.message_handler(commands=['product'])
def deputies(message):
    arg = message.text[9:]
    r = kbot.show_product(arg)
    if len(r) > 4096:
        for x in range(0, len(r), 4096):
            bot.send_message(message.chat.id, r[x:x + 4096])
    else:
        bot.send_message(message.chat.id, r)

if __name__ == '__main__':
    bot.polling()