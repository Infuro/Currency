import json
from policy import Policy
from database import connect, create_table, insert_policies


def load_data():
    with open("configClear_v2.json", 'r') as file:
        data = json.load(file)
        third_level = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]

    return third_level


def main():
    third_level = load_data()

    ix = 1
    table_of_policies = []

    for item in third_level["Port-channel"]:
        id = ix
        name = item.get("name")
        description = item.get("description")
        config = json.dumps(item)
        port_channel_id = "0"
        max_frame_size = item.get("mtu")
        policy_map = Policy(
            id,
            name,
            description,
            config,
            port_channel_id,
            max_frame_size
        )
        table_of_policies.append(policy_map)
        ix += 1

    for item in third_level["TenGigabitEthernet"]:
        id = ix
        name = item.get("name")
        description = item.get("description")
        config = json.dumps(item)
        port_channel_id = "0"
        max_frame_size = item.get("mtu")
        policy_map = Policy(
            id,
            name,
            description,
            config,
            port_channel_id,
            max_frame_size
        )
        table_of_policies.append(policy_map)
        ix += 1

    for item in third_level["GigabitEthernet"]:
        id = ix
        name = item.get("name")
        description = item.get("description")
        config = json.dumps(item)
        port_channel_id = "0"
        max_frame_size = item.get("mtu")
        policy_map = Policy(
            id,
            name,
            description,
            config,
            port_channel_id,
            max_frame_size)
        table_of_policies.append(policy_map)
        ix += 1

    conn = connect()
    cursor = conn.cursor()
    create_table(cursor)
    insert_policies(cursor, table_of_policies)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
