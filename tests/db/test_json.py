from db.json import JSON


def test_congifuration_add(conf):
    JSON.add_configuration(conf)


def test_congifuration_get(device_id):
    conf = JSON.get_device_configurations(device_id)
    print(f'congifuration_info: {conf}')


def test_congifuration_update(conf_id, conf):
    JSON.update_configuration(conf_id, conf)


def test_manager_get(device_id):
    manager_info = JSON.get_manager(device_id)
    print(f'manager_info: {manager_info}')


def test_parent_get(device_id):
    parent_info = JSON.get_parent(device_id)
    print(f'parent_info: {parent_info}')


def test_parent_add(device_id, parent_id):
    JSON.add_parent(device_id, parent_id)


def test_parent_update(device_id, parent_id):
    JSON.update_parent(device_id, parent_id)


def test_space_get(device_id):
    space_info = JSON.get_space(device_id)
    print(f'space_info: {space_info}')


def test_space_add(device_id, params):
    JSON.add_space(device_id, params)


def test_space_update(device_id, params):
    JSON.update_space(device_id, params)


def test_status_get(device_id):
    status_info = JSON.get_status(device_id)
    print(f'status_info: {status_info}')


def test_link_get():
    links = JSON.get_links()
    print(f'links_info: {links}')


def test_link_add(link_info):
    JSON.add_link(link_info)


def test_link_update(link_id, link_info):
    JSON.update_link(link_id, link_info)


def test_model_get(model_type):
    model_info = JSON.get_model(model_type)
    print(f'model_info: {model_info}')


def test_device_get(device_id):
    info = JSON.get_device_info(device_id)
    print(f'device_info: {info}')


def test_device_update(device_id, info):
    JSON.update_device_info(device_id, info)


def test_device_all_info_get(device_id):
    info = JSON.get_device_all_info(device_id)
    print(f'device_all_info: {info}')


if __name__ == '__main__':
    # 测试 all info
    test_device_all_info_get('2')

    # # 测试device
    # test_device_get('2233')
    # test_device_update('2233', {'uuid': '3322'})
    # test_device_get('2233')
    # # 测试model
    # test_model_get('E9000')
    # # 测试link
    # link_info = {
    #   "name": "11<->12",
    #   "device_id_a": "11",
    #   "device_id_b": "12",
    #   "link_type": "DMI",
    #   "link_protocol": "DMI",
    #   "link_protocol_version": "3",
    #   "link_width": "4"
    # }
    # test_link_add(link_info)
    # test_link_get()
    # link_info.update({'link_type': 'test'})
    # test_link_update('1', link_info)
    # # 测试 status
    # test_status_get('1')
    # # 测试parent
    # test_parent_add('2233', {'parent_id': '3322'})
    # test_parent_get('2233')
    # test_parent_update('2233', {'parent_id': '2222'})
    # test_parent_get('2233')
    # # 测试space
    # space = {
    #     'space_type': 'switch',
    #     'name': 'switch slot',
    #     'direction': 'vertical',
    #     'serial': '2'
    # }
    # test_space_add('2233', space)
    # test_space_get('2233')
    # space.update({'serial': '3'})
    # test_parent_update('2233', space)
    # test_space_get('2233')
    # # 测试manager
    # test_manager_get('1')
    # # 测试configuration
    # configuration = {
    #     'device_id': '11',
    #     'type': 'stack',
    #     'params': {
    #         'domain_id': 10,
    #         'member_id': 3,
    #         'priority': 100,
    #         'stack_port': [
    #             {
    #                 'port_id': "1",
    #                 'physical_port': [
    #                     '40GE 3/18/1'
    #                 ]
    #             }
    #         ]
    #     }
    # }
    # test_congifuration_add(configuration)
    # test_congifuration_get('11')
    # configuration.update({'type': 'trunk'})
    # test_congifuration_update('3', configuration)
    # test_congifuration_get('11')
