import requests
import json
import os
import time
from datetime import datetime
import textwrap
import getpass

class DeepSeekChat:
    """
    Класс для взаимодействия с API DeepSeek Chat.
    """
    def __init__(self):
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.conversation_history = []
        self.message_count = 0
        self.api_key = None
        self.config_file = "deepseek_config.json"

    def load_api_key(self):
        """Загружает API ключ из файла конфигурации"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    return True
            return False
        except Exception as e:
            print(f"\033[1;33m⚠️ Предупреждение: Не удалось загрузить конфигурацию: {e}\033[0m")
            return False

    def save_api_key(self, api_key):
        """Сохраняет API ключ в файл конфигурации"""
        try:
            config = {
                'api_key': api_key,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            # Устанавливаем безопасные права доступа к файлу
            os.chmod(self.config_file, 0o600)
            return True
        except Exception as e:
            print(f"\033[1;31m❌ Ошибка при сохранении API ключа: {e}\033[0m")
            return False

    def get_api_key_from_user(self):
        """Запрашивает API ключ у пользователя"""
        self.clear_screen()
        self.print_header()
        
        print("\033[1;36m" + "🔑 Настройка API ключа DeepSeek" + "\033[0m")
        print("\033[1;37m" + "═" * 50 + "\033[0m")
        print()
        print("\033[1;33m📝 Для работы с DeepSeek Chat необходим API ключ.")
        print("   Получить ключ можно по адресу:")
        print("   \033[1;36mhttps://platform.deepseek.com/api_keys\033[1;33m")
        print()
        print("💡 Ключ будет сохранен локально для будущих сессий.")
        print("🔒 Ваши данные защищены и хранятся только на вашем устройстве.")
        print()
        
        while True:
            try:
                api_key = getpass.getpass("\033[1;32m🔐 Введите ваш API ключ: \033[0m").strip()
                
                if not api_key:
                    print("\033[1;31m❌ API ключ не может быть пустым!\033[0m")
                    continue
                
                # Проверяем базовый формат ключа (обычно начинается с sk-)
                if not api_key.startswith('sk-'):
                    print("\033[1;33m⚠️  API ключ обычно начинается с 'sk-'. Проверьте правильность ввода.\033[0m")
                    confirm = input("\033[1;33mПродолжить anyway? (y/N): \033[0m").strip().lower()
                    if confirm != 'y':
                        continue
                
                # Тестируем ключ
                print("\033[1;33m\n🔄 Проверка API ключа...\033[0m")
                if self.test_api_key(api_key):
                    self.api_key = api_key
                    if self.save_api_key(api_key):
                        print("\033[1;32m✅ API ключ успешно сохранен!\033[0m")
                        time.sleep(1)
                    else:
                        print("\033[1;33m⚠️  Ключ работает, но не удалось сохранить его.\033[0m")
                    return True
                else:
                    print("\033[1;31m❌ Неверный API ключ! Пожалуйста, проверьте и попробуйте снова.\033[0m")
                    retry = input("\033[1;33mПопробовать снова? (Y/n): \033[0m").strip().lower()
                    if retry == 'n':
                        return False
                    
            except KeyboardInterrupt:
                print("\n\n\033[1;33m🚪 Выход из программы...\033[0m")
                return False
            except Exception as e:
                print(f"\033[1;31m❌ Ошибка: {e}\033[0m")
                return False

    def test_api_key(self, api_key):
        """Проверяет валидность API ключа"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
            return response.status_code == 200
            
        except requests.exceptions.RequestException:
            return False
        except Exception:
            return False

    def clear_screen(self):
        """Очищает экран терминала"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Выводит красивый заголовок"""
        header = """
⢠⣶⣶⣾⣇⠰⣧⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡟⠛⠿⣿⣟⢷⣽⠏⠁⢠⠄⡇⡤⢤⢀⡤⣄⣤⠤⡄⡤⢤⢠⠤⡄⣠⢤⣸⡇⡤
⢿⡀⠀⠘⣿⣾⡿⠀⠀⢻⣤⡇⢯⣭⠹⣬⡭⣿⣤⠇⣝⣿⠸⣬⡍⢧⣭⢽⡟⣇
⠈⠻⣾⣷⡮⠿⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        print("\033[1;36m" + header + "\033[0m")

    def print_footer(self):
        """Выводит нижнюю часть интерфейса"""
        footer = """
    ════════════════════════════════════════════════════════════════
    💡 Советы: Введите 'clear' для очистки чата, 'quit' для выхода
               'newkey' для смены API ключа, 'menu' для меню
        """
        print("\033[1;35m" + footer + "\033[0m")

    def print_menu(self):
        """Выводит меню дополнительных команд"""
        menu = """
    🎛️  ДОСТУПНЫЕ КОМАНДЫ:
    
    🔑 newkey   - Сменить API ключ
    🗑️  clear    - Очистить историю чата  
    📊 stats    - Показать статистику
    🌀 menu     - Показать это меню
    🚪 quit     - Выйти из программы
    
    ════════════════════════════════════════════════════════════════
        """
        print("\033[1;36m" + menu + "\033[0m")

    def print_stats(self):
        """Выводит подробную статистику диалога"""
        stats = f"""
    📊 СТАТИСТИКА ДИАЛОГА:
    
    💬 Сообщений: {self.message_count // 2}
    👤 Ваши сообщения: {len([m for m in self.conversation_history if m['role'] == 'user'])}
    🤖 Ответов AI: {len([m for m in self.conversation_history if m['role'] == 'assistant'])}
       Текущее время: {datetime.now().strftime('%H:%M:%S')}
        """
        print("\033[1;35m" + stats + "\033[0m")

    def print_typing_animation(self):
        """Анимация печати"""
        animations = [
            "🔮 DeepSeek генерирует ответ",
            "💫 Обрабатываю запрос", 
            "   Анализирую контекст",
            "🌟 Формирую ответ"
        ]
        
        import random
        animation_text = random.choice(animations)
        
        for i in range(3):
            print(f"\r\033[1;33m{animation_text}{'.' * (i + 1)}\033[0m", end="", flush=True)
            time.sleep(0.4)
        print("\r\033[1;33m" + " " * 50 + "\r", end="", flush=True)

    def format_message(self, message, role):
        """Форматирует сообщение для красивого вывода"""
        width = 70
        
        if role == "user":
            color = "\033[1;32m"  # Зеленый для пользователя
            prefix = "👤 ВЫ"
            wrapper = textwrap.TextWrapper(
                width=width, 
                initial_indent=" " * 2, 
                subsequent_indent=" " * 2
            )
        else:
            color = "\033[1;34m"  # Синий для ассистента
            prefix = "🤖 DEEPSEEK"
            wrapper = textwrap.TextWrapper(
                width=width, 
                initial_indent=" " * 2, 
                subsequent_indent=" " * 2
            )
        
        formatted_text = wrapper.fill(message)
        lines = formatted_text.split('\n')
        max_line_length = max(len(line) for line in lines)
        
        print(f"{color}╔{'═' * (max_line_length + 4)}╗\033[0m")
        print(f"{color}║ {prefix:<{max_line_length + 2}} ║\033[0m")
        print(f"{color}╠{'═' * (max_line_length + 4)}╣\033[0m")
        
        for line in lines:
            padded_line = line.ljust(max_line_length)
            print(f"{color}║ {padded_line}  ║\033[0m")
        
        print(f"{color}╚{'═' * (max_line_length + 4)}╝\033[0m")
        print()

    def send_message(self, message):
        """
        Отправляет сообщение пользователя в API и возвращает ответ ассистента.
        """
        if not self.api_key:
            return "API ключ не установлен. Используйте команду 'newkey'."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.conversation_history.append({"role": "user", "content": message})

        data = {
            "model": "deepseek-chat",
            "messages": self.conversation_history,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            self.print_typing_animation()
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            
            if not result.get("choices"):
                return "API вернул пустой ответ."
                
            assistant_message = result["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            self.message_count += 2

            return assistant_message

        except requests.exceptions.Timeout:
            return "⏰ Таймаут запроса. Попробуйте снова."
        except requests.exceptions.RequestException as e:
            return f"Ошибка сети: {e}"
        except KeyError as e:
            return f"Ошибка в структуре ответа: {e}"
        except Exception as e:
            return f"Непредвиденная ошибка: {e}"

    def clear_chat(self):
        """Очищает историю чата"""
        self.conversation_history.clear()
        self.message_count = 0
        print("\033[1;32m" + "🗑️ История чата очищена!" + "\033[0m")
        time.sleep(1)

    def change_api_key(self):
        """Позволяет пользователю сменить API ключ"""
        print("\033[1;33m🔄 Смена API ключа...\033[0m")
        if self.get_api_key_from_user():
            self.clear_chat()
            return True
        return False

    def get_user_input(self):
        """Красивый ввод от пользователя"""
        prompt = "\033[1;32m💬 Ваше сообщение: \033[0m"
        try:
            user_input = input(prompt).strip()
            return user_input
        except KeyboardInterrupt:
            raise
        except Exception:
            return ""

    def initialize(self):
        """Инициализирует приложение с загрузкой или запросом API ключа"""
        self.clear_screen()
        self.print_header()
        
        print("\033[1;36m" + "🚀 Загрузка DeepSeek Chat..." + "\033[0m")
        time.sleep(1)
        
        # Пытаемся загрузить сохраненный API ключ
        if self.load_api_key():
            print("\033[1;32m   API ключ загружен из сохраненной конфигурации\033[0m")
            time.sleep(1)
            return True
        else:
            print("\033[1;33m📝 API ключ не найден. Требуется настройка.\033[0m")
            time.sleep(1)
            return self.get_api_key_from_user()

    def run(self):
        """
        Основной цикл для взаимодействия с пользователем.
        """
        if not self.initialize():
            return

        self.clear_screen()
        self.print_header()
        print("\033[1;36m" + " Готов к общению! Введите 'menu' для списка команд." + "\033[0m")
        print()

        while True:
            try:
                user_input = self.get_user_input()

                # Обработка специальных команд
                if user_input.lower() in ['quit', 'exit', 'выход']:
                    self.clear_screen()
                    self.print_header()
                    print("\033[1;33m" + "👋 Спасибо за общение! Возвращайтесь снова!" + "\033[0m")
                    break
                
                elif user_input.lower() in ['clear', 'очистить']:
                    self.clear_chat()
                    self.clear_screen()
                    self.print_header()
                    print("\033[1;36m" + "💬 Чат очищен. Продолжаем общение!" + "\033[0m")
                    continue
                
                elif user_input.lower() in ['newkey', 'ключ']:
                    self.change_api_key()
                    self.clear_screen()
                    self.print_header()
                    print("\033[1;36m" + " Ключ обновлен! Продолжаем общение." + "\033[0m")
                    continue
                
                elif user_input.lower() in ['menu', 'help', 'помощь']:
                    self.clear_screen()
                    self.print_header()
                    self.print_menu()
                    continue
                
                elif user_input.lower() in ['stats', 'статистика']:
                    self.clear_screen()
                    self.print_header()
                    self.print_stats()
                    self.print_footer()
                    continue
                
                elif not user_input:
                    continue

                # Обычное сообщение - обрабатываем через API
                self.format_message(user_input, "user")
                response = self.send_message(user_input)
                self.format_message(response, "assistant")
                self.print_footer()

            except KeyboardInterrupt:
                print("\n\n\033[1;33m" + "👋 Прервано пользователем. До свидания!" + "\033[0m")
                break
            except Exception as e:
                print(f"\033[1;31m  Критическая ошибка: {e}\033[0m")
                break

if __name__ == "__main__":
    chat = DeepSeekChat()
    chat.run()