class Human:      # Player, Fan 클래스가 중복해서 가지는 속성(name)과 메서드(sayhello())를 가짐
    def __init__(self, name):
        self.name = name
    def say_hello(self):
        print(f"hello my name is {self.name}")


# 2.1. __init__()
class Player(Human):                # Human 클래스 상속
    def __init__(self, name, xp):   # init 메서드는 클래스 생성 시 자동 호출 됨 (클래스 초기화)
        super().__init__(name)
        # self.name = name          # self 인자는 class를 가리킴
        self.xp = xp
    # def say_hello(self):
    #     print(f"hello my name is {self.name}")

# yunna = Player("yunna", 1000)
# yunna.say_hello()


# 2.2. inheritance (상속) 
# -> Human class를 추가함 
# super 함수는 부모 클래스에 접근할 권한을 줌 
class Fan(Human):
    def __init__(self, name, fav_team):   # 여기서 받은 name을 부모 클래스로 전달해줘야 함(그래야 Human class의 init 메서드가 name을 받아 실행됨) -> super사용
        super().__init__(name)   # super().__init__()는 Human.__init__()과 같고, 부모 클래스에 필요한 인자(name)을 넘겨줌, 넘겨줄 인자가 필요 없으면 super()~ 안해도 됨
        # self.name = name
        self.fav_team = fav_team
    # def say_hello(self):
    #     print(f"hello my name is {self.name}")

yunna_player = Player("yunna", 10)  # 이 코드는 Player의 init 메서드를 호출호는 것과 같아
yunna_fan = Fan("yunna_fan", "dontknow")

yunna_player.say_hello()
yunna_fan.say_hello()


# 2.3. recap
# super, init 필요 없는 경우 (받을 속성, 인자가 있는 경우에만 사용)
class Dog:
    def woof(self):
        print("woof woof")

class Beagle(Dog):
    def jump(self):
        print("jump")
    def woof(self):          # 메서드 오버라이딩 (부모 클래스의 같은 메서드를 다르게 사용하고 싶어)
        super().woof()       # super를 항상 init 메서드만 호출하는 용도로 사용하진 않아
        print("super woof")  # super(dog)의 woof woof 출력 후, super woof 출력할 것

beagle = Beagle()
beagle.woof()


# 2.4. 클래스의 underscore 함수들
class Dog:
    def __init__(self, name):    # init 메서드만 있을 경우 jia를 print하면 <__main__.Dog object at 0x000001D12C53FE48>가 출력됨
        self.name = name         # jia는 Dog 객체이고, 0x000001D12C53FE48의 메모리상에 있다.

    def __str__(self):             # __str__() 메서드는 해당 클래스의 메모리 주소값을 반환하는데, 이걸 우리는 doggy!라고 쓰겠다 (메서드 오버라이딩), 클래스가 문자열로써 어떻게 보일지를 결정해줌
        print(super().__str__())   # 이 코드는 최상위 클래스인 object 클래스의 __str__을 프린트하므로 똑같이 <__main__.Dog object at 0x000001D12C53FE48> 출력
        return "doggy!"            # 모든 클래스는 최상위 클래스인 object 클래스를 상속함(보이지 않음), 이 object 클래스에 있는 메서드가 __init__, __Str__, .. 등
    def __getattribute__(self, name):   # 속성에 접근할 수 있게 해줌, 속성을 어떻게 다뤄서 보여줄 지 커스텀할 수 있음
        return "@@"                     # 이것도 오버라이딩.. 


jia = Dog("jia")    # __str__ 메서드를 호출하지 않아도 파이썬 내부적으로 실행시킴
print(jia)          # str 메서드를 사용함으로써 메모리 주소값이 아닌 doggy!를 출력
print(jia.name)     # print(jia.name) 하면 name인 jia를 출력하지 않고 @@를 출력


