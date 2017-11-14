from db.restful import RESTFul


def test_set_conf(conf):
    RESTFul.set_conf(conf)
    print(f'conf is {conf}')
    print(f'RESTFul conf is {RESTFul.prefix}')


def test_congifuration_add(conf):
    print(f'add configuration {conf}')
    RESTFul.add_configuration(conf)


def test_congifuration_get(device_id):
    conf = RESTFul.get_device_configurations(device_id)
    print(f'congifuration_info of {device_id}: {conf}')


def test_congifuration_update(conf_id, conf):
    print(f'update configuration of {conf_id}: {conf}')
    RESTFul.update_configuration(conf_id, conf)


def test_manager_get(device_id):
    res = RESTFul.get_manager(device_id)
    print(f'get managers of {device_id}: {res}')


def test_parent_and_space_get(device_id):
    res = RESTFul.get_parent_and_space(device_id)
    print(f'get parent of {device_id}: {res["parent_id"]}')
    print(f'get space of {device_id}: {res["space"]}')


def test_parent_and_space_update(device_id, parent_id, space_info):
    print(f'update parent of {device_id}: {parent_id}')
    print(f'update space of {device_id}: {space_info}')
    RESTFul.update_parent_and_space(device_id, parent_id, space_info)


def test_parent_and_space_add(device_id, parent_id, space_info):
    print(f'update parent of {device_id}: {parent_id}')
    print(f'update space of {device_id}: {space_info}')
    RESTFul.add_parent_and_space(device_id, parent_id, space_info)


def test_links_get():
    links = RESTFul.get_links()
    print(f'links_info: {links}')


def test_link_update(link_id, link_info):
    print(f'update link of {link_id}: {link_info}')
    RESTFul.update_link(link_id, link_info)


def test_link_add(link_info):
    print(f'add link: {link_info}')
    RESTFul.add_link(link_info)


def test_device_info_get(device_id):
    device_info = RESTFul.get_device_info(device_id)
    print(f'get device_info of {device_id}: {device_info}')


def test_device_info_update(device_id, device_info):
    print(f'update device_info of {device_id}: {device_info}')
    RESTFul.update_device_info(device_id, device_info)


def test_device_all_info_get(device_id):
    device_info = RESTFul.get_device_all_info(device_id)
    print(f'get devie <{device_id}> all info: {device_info}')


def test_device_all_info_update(device_id, info):
    print(f'update device <{device_id}> all info: {info}')
    res = RESTFul.update_device_all_info(device_id, info)
    print(res)


if __name__ == '__main__':
    # 测试 set_conf
    conf = {
        'db_version': '2017.11.10',
        'db_host': '127.0.0.1',
        'db_port': '8081',
        'db_protocol': 'http',
        'db_type': 'restful'
    }
    test_set_conf(conf)
    # 测试all
    all_info = {
        'model': 'processor',
        'device': {
            'id': '234',
            'description': 'Second CPU',
            'name': 'cpu 2',
            'model_type': 'Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz'
        },
        'status': {
            'state': 'Enable',
            'health': 'OK'
        },
        'space': {
            'id': '584c654a-35a0-40bb-be02-8b7ad8211cf0',
            'space_type': 'update',
            'name': 'test1',
            'direction': 'test',
            'serial': 'test',
            'x': '11',
            'y': '2',
            'z': '3',
            'data_center': 'test'
        },
        'part': {
            'parent_id': '17fc9612-051a-42b7-a5b9-26e4121f8239'
        }
    }
    # test_device_all_info_get('f61faf4c-4ed6-4f13-a7c1-757ebdc12827')
    # test_device_all_info_update('f61faf4c-4ed6-4f13-a7c1-757ebdc12827',all_info)
    # 测试device
    test_device_info_update('17fc9612-051a-42b7-a5b9-26e4121f8239', all_info)
    # test_device_info_get('17fc9612-051a-42b7-a5b9-26e4121f8239')

    # 测试link
    # link_info = {
    #     "name": "2<->3",
    #     "device_id_a": "2",
    #     "device_id_b": "3",
    #     "port_a": "40GE2/18/1",
    #     "port_b": "40GE3/18/1",
    #     "link_type": "Optical",
    #     "usage": "Stack"
    # }
    # test_link_add(link_info)
    # test_links_get()
    # link_info.update({"usage": "Trunk"})
    # test_link_update('1', link_info)
    # test_links_get()

    # 测试Manager
    # test_manager_get('b0a8c620-04ca-4f8e-adaa-3570379fb326')

    # 测试Space and Parent
    # test_parent_and_space_get('f61faf4c-4ed6-4f13-a7c1-757ebdc12827')
    # space_info = {
    #     'space_type': 'update',
    #     'name': 'test1',
    #     'direction': 'test',
    #     'serial': 'test',
    #     'x': '1',
    #     'y': '2',
    #     'z': '3',
    #     'data_center': 'test'
    # }
    # test_parent_and_space_update('f61faf4c-4ed6-4f13-a7c1-757ebdc12827', '17fc9612-051a-42b7-a5b9-26e4121f8239',
    #                              space_info)
    # test_parent_and_space_add('5eef4c17-af7c-43d9-8b85-161c6ffdc5e3','17fc9612-051a-42b7-a5b9-26e4121f8239', space_info)

    # 测试configuration
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
