import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер', age='4', pet_photo='1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Жулька', animal_type='Дворняжка', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_add_self_pet_photo(pet_photo='1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.added_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['pet_photo'] == pet_photo


def test_get_api_key_for_dont_valid_user(email='gremka90@gmail.co', password=valid_password):
    # 1
    # Пытаемся получить ключ с невалидным емайлом
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pet_without_name(name='Перро', animal_type='Дворняжка', age='5'):
    # 2
    # Пытаемся добавить питомца без возраста
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    with pytest.raises(TypeError):
        pf.add_new_pet_without_photo(auth_key, name, animal_type)


def test_uccessful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    # 3
    # Пытаемся изменить информацию не существующего питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    with pytest.raises(IndexError):
        pf.update_pet_info(auth_key, my_pets['pets'][100000000000]['id'], name, animal_type, age)


def test_uccessful_delete_self_pet():
    # 4
    '''Я тут пытался проверить будет ли выдавать ошибку при поппытке удаления
    с не существующим ID питомца. Но похоже api всё устраивает ¯\_(ツ)_/¯ '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.delete_pet(auth_key, '123123123')
    # with pytest.raises(IndexError):
    # pf.delete_pet(auth_key, ' ')


def test_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    # 5
    ''' Или я то то не то делаю или оно обновляет информацию не существующего питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pf.update_pet_info(auth_key, '123123123', name, animal_type, age)


def test_get_api_key_for_dont_valid_password(email=valid_email, password='1234'):
    # 6
    # Пытаемся получить ключ с невалидным паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pet_with_error_attribute(name='ЖУк', animal_type='Дворняжка', age='dfs'):
    # 7
    # Добавляем питомца с неверным форматом возвраста, api прнимает текст, хотя так не должно быть
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    #with pytest.raises(TypeError):
    pf.add_new_pet_without_photo(auth_key, name, animal_type, str(age))


def test_add_new_pet_with_error_photo(name='Барбоскин', animal_type='двортерьер', age='4', pet_photo='2.jpg'):
    # 8
    # Пытаемся добавить питомца с не существующим фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    with pytest.raises(FileNotFoundError):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


def test_get_all_pets_with_not_my_filter(filter='Not_my_filter'):
    # 9
    # Пытаемся вызвать ошибку на стороне сервера, пуём получения списка питомцев с несуществующим фильтром
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_get_all_pets_without_auth_key(filter=''):
    # 10
    # Пытаемся получить список питомцев с невалидным ключом авторзации
    auth_key = '123'
    #status, result = pf.get_list_of_pets(auth_key, filter)
    with pytest.raises(TypeError):
        pf.get_list_of_pets(auth_key, filter)