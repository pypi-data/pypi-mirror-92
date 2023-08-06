# EDECS
Event-driven Entity-Component-System engine

ECS-фреймворк на базе событий

---

## Установка

```
pip install edecs
```

## Философия

Данные отделены от логики и разделены между собой на сущности и компоненты. Вся логика реализуется в системах. Системы общаются между собой событиями.

Сущность - просто контейнер для компонентов.

Компоненты отражают свойства сущности. Например, можно создать компонент "Здоровье" и закрепить его за сущностью "Игрок".

Системы - объекты, реализующие всю игровую логику. Могут генерировать и принимать события.

## [Документация](https://github.com/Laminariy/edecs/blob/master/docs.md)

## [Примеры кода](https://github.com/Laminariy/edecs-examples)

## Краткий гайд

### Компонент (Component)

Небольшой набор данных, отвечающих за то или иное свойство сущности.

Пример:

```python
from edecs import Component

class HealthComponent(Component):
    # стандартные значения данных компонента:
    defaults = {
        'max_hp': 10,
        'hp': 10
    }
```

Это компонент "здоровья" сущности. Он хранит в себе максимально допустимый и текущий уровень здоровья.

---

```python
from random import random
from edecs import Component

class AttackComponent(Component):
    defaults = {
        'damage': 1,
        'crit_damage': 3,
        'crit_chance': 0.3,
        'target': -1 # id цели, которую существо атакует
    }
    
    # функция рассчета урона
    def get_damage(self):
        if random() <= self.crit_chance:
            return self.crit_damage
        
        return self.damage
```

Компонент, отвечающий за данные об атаке. Здесь можно увидеть, как можно обращаться к данным внутри компонента - как к обычным атрибутам класса.

Так же мы добавили здесь функцию, которая, в зависимости от рандом-генератора возвращает нанесенный урон - обычный или критический. Однако нужно помнить, что компоненты - это просто данные, и не нужно прописывать в них какую либо сложную логику. В данном случае мы просто работаем с данными самого компонента и немного упрощаем дальнейшую работу, так что в этом нет ничего страшного.

### Сущность (Entity)

Контейнер для компонентов. Сам по себе ничего не представляет - это просто объект, знающий свой идентификатор, тип и имя. Чтобы добавить сущности свойство, необходимо добавить ей компоненты.

Пример:

```python
from edecs import Entity
from health_component import HealthComponent
from attack_component import AttackComponent

class Skeleton(Entity):
    # стандартные компоненты сущности:
    default_components = {
        'health': HealthComponent(max_hp=5, hp=5),
        'attack': AttackComponent()
    }
```

Сущность, отображающая игрового персонажа - скелета. Мы добавили ей компонент здоровья, созданный на предыдущем шаге, и установили начальные значения для параметров. Так же мы добавили компонент атаки. Значения атрибутов остались по умолчанию теми же, что мы и указывали на предыдущем пункте.

---

```python
from edecs import Entity
from health_component import HealthComponent
from attack_component import AttackComponent

class Hero(Entity):
    default_components = {
        'health': HealthComponent(max_hp=20, hp=20),
        'attack': AttackComponent(damage=3, crit_damage=5, crit_chance=0.45)
    }
```

Сущность героя. Имеет те же компоненты, что и скелет, но измененные значения (Это же герой, он должен быть сильным!)

### Система (System)

Системы используются для реализации той или иной логики.


Пример:

```python
from edecs import System
from skeleton import Skeleton
from hero import Hero

class CombatSystem(System):
    # init() вызывается при создании системы
    def init(self):
        # создаем объекты сущностей
        hero = Hero('Brave Knight')
        skeleton = Skeleton('Archer Skeleton')

        # добавляем их в "мир"
        self.create_entity(hero)
        self.create_entity(skeleton)

        # "натравливаем" друг на друга - добавляем айди в компонент атаки
        hero.attack.target = skeleton.id
        skeleton.attack.target = hero.id

        # подписываем функцию на событие смерти
        self.subscribe(self.on_death, 'DeathEvent')

    # событие о смерти персонажа
    def on_death(self, event):
        id = event.id

        # удаляем мертвую сущность
        death_entity = self.entity_manager.entities[id]
        self.destroy_entity(death_entity)

    # update() вызывается каждый проход игрового цикла
    def update(self, dt):
        # находим все компоненты атаки и здоровья
        attack_components = self.component_manager.component_types['AttackComponent']
        health_components = self.component_manager.component_types['HealthComponent']

        # пробегаем все компоненты атаки
        for id, atk in attack_components.items():
            target_id = atk.target

            if target_id == -1:
                break # если существо никого не атакует - ничего не делаем, выходим из цикла

            # рассчитываем урон и вычитаем здоровье
            damage = atk.get_damage()
            health_components[target_id].hp -= damage

            # отправляем событие, что один персонаж атаковал другого
            self.generate_event('AttackEvent', {'attacker_id':id, 'target_id':target_id, 'damage':damage})

            # если цель умерла после атаки
            if health_components[target_id].hp <= 0:
                # отправляем событие о смерти персонажа
                name = self.entity_manager.entities[target_id].name
                self.generate_event('DeathEvent', {'id':target_id,'name':name})

                # убираем цель атакующему
                atk.target = -1

                # так как умершее существо еще не удалено системой, уберем и у него цель тоже
                attack_components[target_id].target = -1
```

Боевая система. Каждый проход игрового цикла находит всех атакующих (по компонентам атаки), рассчитывает урон и применяет его к цели атакующего.

---

```python
from edecs import System

class LogSystem(System):
    # log() вызовется когда случится событие, на которое подписана эта функция
    def log(self, event):
        # если пришло событие об атаке, то выводим сообщение в консоль
        if event.type == 'AttackEvent':
            attacker_id = event.attacker_id
            target_id = event.target_id
            damage = event.damage

            attacker_name = self.entity_manager.entities[attacker_id].name
            target_name = self.entity_manager.entities[target_id].name

            print("%s наносит %s урона персонажу %s!" % (attacker_name, damage, target_name))

        # если кто-то умер
        elif event.type == 'DeathEvent':
            print("Персонаж %s умер!" % event.name)

    # здесь в init() мы подписываем функцию log() на события
    def init(self):
        self.subscribe(self.log, 'AttackEvent')
        self.subscribe(self.log, 'DeathEvent')
```
Система логирования, которая будет выводить в консоль события.

### Движок (Engine)

```python
from edecs import Engine
from systems import (CombatSystem, LogSystem)

def main():
    # создаем объект движка
    engine = Engine()
    
    # создаем системы
    engine.create_system(CombatSystem())
    engine.create_system(LogSystem())
    
    # игровой цикл
    while True:
        engine.update()
    
if __name__ == '__main__':
    main()
```

Движок является управляющим объектом всего edecs. Через него можно влиять на внутренние данные и системы, отправлять или получать события.
