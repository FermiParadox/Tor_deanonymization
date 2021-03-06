from ipaddress import ip_address
from unittest import TestCase

from analysis.itxyek_base import ITXYEK
from analysis.user_base import User
from analysis.user_handling import AllUsers

TOR_USER_TIMES = [1638636528300, 1638636528300, 1638636528300, 1638636528400, 1638636528400, 1638636528400,
                  1638636528400, 1638636528400, 1638636528400, 1638636528500, 1638636528500, 1638636528500,
                  1638636528500, 1638636528500, 1638636528500, 1638636528600, 1638636528600, 1638636528600,
                  1638636528600, 1638636528600, 1638636528600, 1638636528600, 1638636528700, 1638636528700,
                  1638636528700, 1638636528700]

NORMAL_USER_TIMES = [1638636689730, 1638636689747, 1638636689764, 1638636689781, 1638636689797,
                     1638636689814, 1638636689830, 1638636689846, 1638636689863, 1638636689880,
                     1638636689897, 1638636689913, 1638636689930, 1638636689946, 1638636689964,
                     1638636689979, 1638636689997, 1638636690013, 1638636690029, 1638636690046,
                     1638636690063, 1638636690080, 1638636690097, 1638636690113, 1638636690130,
                     1638636690163, 1638636690180, 1638636690196, 1638636690213, 1638636690230,
                     1638636690310, 1638636690330, 1638636690346, 1638636690363, 1638636690380,
                     1638636690398]


class TestIsTorUser(TestCase):
    def setUp(self) -> None:
        from analysis.user_base import User
        self.user = User(id=93847629346,
                         ip=ip_address("0.0.0.0"),
                         all_itxyek=ITXYEK([5, 6, 7], [1, 2, 3], [11, 22, 33], [111, 222, 333]))

    def test_false(self):
        from analysis.user_handling import is_tor_user

        self.user.all_itxyek.time = NORMAL_USER_TIMES
        self.assertFalse(is_tor_user(user=self.user))

    def test_true(self):
        from analysis.user_handling import is_tor_user

        self.user.all_itxyek.time = TOR_USER_TIMES
        self.assertTrue(is_tor_user(user=self.user))


class TestCombinations(TestCase):
    def setUp(self) -> None:
        from analysis.user_handling import Combinations
        from analysis.user_base import User
        self.Combinations = Combinations
        self.u1 = User(id=93847629346,
                       ip=ip_address("0.0.0.0"),
                       all_itxyek=ITXYEK([5, 6, 7], [1, 2, 3], [11, 22, 33], [111, 222, 333]))

        self.u2 = User(id=34574574734,
                       ip=ip_address("127.0.5.0"),
                       all_itxyek=ITXYEK([5, 6, 7], [1, 2, 3], [11, 22, 33], [111, 222, 333]))

        self.u3 = User(id=12346346468,
                       ip=ip_address("87.25.6.0"),
                       all_itxyek=ITXYEK([5, 6, 7], [1, 2, 3], [11, 22, 33], [111, 222, 333]))

    def test_2_users_1_combinations(self):
        combs = self.Combinations.all_user_combs([self.u1, self.u2])
        self.assertEqual(1, len(list(combs)))

    def test_3_users_3_combinations(self):
        combs = self.Combinations.all_user_combs([self.u1, self.u2, self.u3])
        self.assertEqual(3, len(list(combs)))

    def test_3_users_1tor_2_combinations(self):
        self.u1.all_itxyek.time = TOR_USER_TIMES
        combs = {(self.u1, self.u2), (self.u1, self.u3), (self.u2, self.u3)}
        tor_combs = self.Combinations._tor_user_combs(combs)
        self.assertEqual(2, len(tor_combs))

    def test_3_users_2tor_3_combinations(self):
        self.u1.all_itxyek.time = TOR_USER_TIMES
        self.u2.all_itxyek.time = TOR_USER_TIMES
        combs = {(self.u1, self.u2), (self.u1, self.u3), (self.u2, self.u3)}
        tor_combs = self.Combinations._tor_user_combs(combs)
        self.assertEqual(3, len(tor_combs))


class TestAllUsers(TestCase):
    def setUp(self) -> None:
        self.u1 = User(id=111,
                       ip=ip_address("0.42.0.0"),
                       all_itxyek=ITXYEK())

        self.u2 = User(id=3333,
                       ip=ip_address("0.0.7.0"),
                       all_itxyek=ITXYEK())

        self.u3_initial = User(id=5252525,
                               ip=ip_address("52.0.0.0"),
                               all_itxyek=ITXYEK())

        self.txy_updated = ITXYEK([66, 33], [1, 2], [11, 22], [111, 222])
        self.u3_updated = User(id=5252525,
                               ip=ip_address("52.0.0.0"),
                               all_itxyek=self.txy_updated)

    def test_displayed_id_exists_when_adding_user(self):
        stored_user = self.u1

        users_list = AllUsers()
        users_list.add(stored_user)

        self.assertEqual(users_list.ids.pop(), str(stored_user.id))

    def test_displayed_ip_exists_when_adding_user(self):
        stored_user = self.u1

        users_list = AllUsers()
        users_list.add(stored_user)

        self.assertEqual(users_list.ips.pop(), str(stored_user.ip))

    def test_all_ids_added_when_unique(self):
        users_list = AllUsers()

        users_list.add(self.u1)
        users_list.add(self.u2)
        users_list.add(self.u3_initial)

        self.assertEqual(len(users_list), 3)

    def test_no_duplicate_ids(self):
        users_list = AllUsers()

        users_list.add(self.u3_initial)
        users_list.add(self.u3_updated)

        self.assertEqual(len(users_list), 1)

    def test_previous_user_data_replaced(self):
        users_list = AllUsers()

        users_list.add(self.u3_initial)
        users_list.add(self.u3_updated)

        user = users_list.pop()
        self.assertEqual(user.all_itxyek, self.txy_updated)
