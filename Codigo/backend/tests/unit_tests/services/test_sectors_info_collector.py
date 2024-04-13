import pytest

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.rel_setor_currency_base_info import SetorCurrencyBaseInfo
from src.models.db.setor import Setor
from src.services.sectors_info_collector import SectorsCollector
from tests.db.db_fixture import test_session


@pytest.fixture(scope="function")
def crypto_on_database(test_session):
    class Crypto:
        def __init__(self):
            self.session = test_session

        def add_to_database(self):
            coin = CurrencyBaseInfoModel(
                symbol="BTC",
                cmc_id=1,
                cmc_slug="bitcoin",
                logo="https://bitcoin.com",
                name="Bitcoin",
                description="The first cryptocurrency",
                technical_doc=["https://bitcoin.com/technical"],
                urls=["https://bitcoin.com"],
            )
            self.session.add(coin)
            self.session.commit()
            self.session.refresh(coin)

            coin2 = CurrencyBaseInfoModel(
                symbol="ETH",
                cmc_id=2,
                cmc_slug="ethereum",
                logo="https://ethereum.com",
                name="Ethereum",
                description="The second cryptocurrency",
                technical_doc=["https://ethereum.com/technical"],
                urls=["https://ethereum.com"],
            )
            self.session.add(coin2)
            self.session.commit()
            self.session.refresh(coin2)

            return [coin, coin2]

    return Crypto()


# @pytest.mark.skip
def test_collect_sectors_with_valid_coins(test_session, crypto_on_database):
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 0
    assert len(test_session.query(Setor).all()) == 0

    crypto_on_database.add_to_database()
    sut = SectorsCollector()
    sut.collect(test_session)

    assert len(test_session.query(SetorCurrencyBaseInfo).all()) > 0
    assert len(test_session.query(Setor).all()) > 0


# @pytest.mark.skip
def test_collect_sectors_with_no_coins_on_database_should_keep_empty(test_session):
    assert len(test_session.query(CurrencyBaseInfoModel).all()) == 0
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 0
    assert len(test_session.query(Setor).all()) == 0

    sut = SectorsCollector()
    sut.collect(test_session)

    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 0
    assert len(test_session.query(Setor).all()) == 0


def test_create_new_sector_on_db_successfully(mocker, test_session, crypto_on_database):
    cryptos = crypto_on_database.add_to_database()
    sut = SectorsCollector()

    db_sectors = test_session.query(Setor).all()
    db_secotors_relations = test_session.query(SetorCurrencyBaseInfo).all()

    assert len(db_sectors) == 0
    assert len(db_secotors_relations) == 0

    sector = [
        {"name": "sector_name", "title": "sector_title", "num_tokens": 25, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
        {"name": "sector_name2", "title": "sector_title2", "num_tokens": 10, "cmc_id": 2, "symbols": ["BTC", "ETH"]},
    ]

    mocker.patch.object(sut.external_collector, "_collect", return_value=sector)
    mocker.patch.object(sut.repository, "get_sector_by_cmc_id", return_value=None)

    sut.collect(test_session)

    db_sectors = test_session.query(Setor).all()
    db_secotors_relations = test_session.query(SetorCurrencyBaseInfo).all()

    for db_sector in db_sectors:
        assert db_sector.coins_quantity >= 10
        assert db_sector.active == True

    for db_sector_relation in db_secotors_relations:
        assert db_sector_relation.uuid_currency in [cryptos[0].uuid, cryptos[1].uuid]
        assert db_sector_relation.uuid_setor in [db_sectors[0].uuid, db_sectors[1].uuid]

    assert len(test_session.query(Setor).all()) == 2
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 4


# @pytest.mark.skip
def test_create_new_sector_when_sector_db_is_none_and_passed_min_coins(mocker, test_session, crypto_on_database):
    cryptos = crypto_on_database.add_to_database()
    sut = SectorsCollector()

    sector = [
        {"name": "sector_name", "title": "sector_title", "num_tokens": 25, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
        {"name": "sector_name2", "title": "sector_title2", "num_tokens": 10, "cmc_id": 2, "symbols": ["BTC", "ETH"]},
    ]

    mocker.patch.object(sut.external_collector, "_collect", return_value=sector)
    mocker.patch.object(sut.repository, "get_sector_by_cmc_id", return_value=None)

    sut.collect(test_session)

    db_sectors = test_session.query(Setor).all()
    db_secotors_relations = test_session.query(SetorCurrencyBaseInfo).all()

    for db_sector in db_sectors:
        assert db_sector.coins_quantity >= 10
        assert db_sector.active == True

    for db_sector_relation in db_secotors_relations:
        assert db_sector_relation.uuid_currency in [cryptos[0].uuid, cryptos[1].uuid]
        assert db_sector_relation.uuid_setor in [db_sectors[0].uuid, db_sectors[1].uuid]

    assert len(test_session.query(Setor).all()) == 2
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 4


# @pytest.mark.skip
def test_deactivate_sector_when_sector_db_exists_and_not_passed_min_coins(mocker, test_session, crypto_on_database):
    cryptos = crypto_on_database.add_to_database()
    sut = SectorsCollector()

    sector = [
        {"name": "sector_name", "title": "sector_title", "num_tokens": 25, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
        {"name": "sector_name2", "title": "sector_title2", "num_tokens": 10, "cmc_id": 2, "symbols": ["BTC", "ETH"]},
    ]

    # add to db sectors
    for sec in sector:
        test_session.add(
            Setor(name=sec["name"], title=sec["title"], coins_quantity=sec["num_tokens"], cmc_id=sec["cmc_id"])
        )
        test_session.commit()

        for symbol in sec["symbols"]:  # type: ignore
            crypto = test_session.query(CurrencyBaseInfoModel).filter(CurrencyBaseInfoModel.symbol == symbol).first()
            sector_uuid = test_session.query(Setor).filter(Setor.cmc_id == sec["cmc_id"]).first().uuid
            test_session.add(SetorCurrencyBaseInfo(uuid_setor=sector_uuid, uuid_currency=crypto.uuid))
            test_session.commit()

    for sec in test_session.query(Setor).all():
        assert sec.active == True  # type: ignore

    db_sectors = test_session.query(Setor).all()
    db_sectors_relations = test_session.query(SetorCurrencyBaseInfo).all()
    sector_name_db = db_sectors[0]
    sector_name_relations = [x for x in db_sectors_relations if x.uuid_setor == sector_name_db.uuid]

    assert sector_name_db.active == True
    assert sector_name_db.coins_quantity == 25
    assert len(sector_name_relations) == 2
    assert len(test_session.query(Setor).all()) == 2
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 4

    mocker.patch.object(
        sut.external_collector,
        "_collect",
        return_value=[
            {"name": "sector_name", "title": "sector_title", "num_tokens": 9, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
            {
                "name": "sector_name2",
                "title": "sector_title2",
                "num_tokens": 10,
                "cmc_id": 2,
                "symbols": ["BTC", "ETH"],
            },
        ],
    )

    sut.collect(test_session)

    db_sectors = test_session.query(Setor).all()
    db_sectors_relations = test_session.query(SetorCurrencyBaseInfo).all()
    sector_name_db = db_sectors[0]
    sector_name_relations = [x for x in db_sectors_relations if x.uuid_setor == sector_name_db.uuid]

    assert sector_name_db.active == False
    assert sector_name_db.coins_quantity == 9
    assert len(sector_name_relations) == 0
    assert len(db_sectors) == 2
    assert len(db_sectors_relations) == 2


def test_activate_sector_when_sector_db_exists_deactivated_and_passed_min_coins(
    mocker, test_session, crypto_on_database
):
    cryptos = crypto_on_database.add_to_database()
    sut = SectorsCollector()

    sector = [
        {"name": "sector_name", "title": "sector_title", "num_tokens": 25, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
        {"name": "sector_name2", "title": "sector_title2", "num_tokens": 10, "cmc_id": 2, "symbols": ["BTC", "ETH"]},
    ]

    # add to db sectors
    for sec in sector:
        test_session.add(
            Setor(name=sec["name"], title=sec["title"], coins_quantity=sec["num_tokens"], cmc_id=sec["cmc_id"])
        )
        test_session.commit()

        for symbol in sec["symbols"]:  # type: ignore
            crypto = test_session.query(CurrencyBaseInfoModel).filter(CurrencyBaseInfoModel.symbol == symbol).first()
            sector_uuid = test_session.query(Setor).filter(Setor.cmc_id == sec["cmc_id"]).first().uuid
            test_session.add(SetorCurrencyBaseInfo(uuid_setor=sector_uuid, uuid_currency=crypto.uuid))
            test_session.commit()

    for sec in test_session.query(Setor).all():
        assert sec.active == True  # type: ignore

    mocker.patch.object(
        sut.external_collector,
        "_collect",
        return_value=[
            {"name": "sector_name", "title": "sector_title", "num_tokens": 30, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
            {
                "name": "sector_name2",
                "title": "sector_title2",
                "num_tokens": 5,
                "cmc_id": 2,
                "symbols": ["BTC", "ETH"],
            },
        ],
    )

    sut.collect(test_session)

    db_sectors = test_session.query(Setor).all()
    db_sectors_relations = test_session.query(SetorCurrencyBaseInfo).all()
    sector_name_db = db_sectors[0]
    sector_name_2_db = db_sectors[1]
    sector_name_relations = [x for x in db_sectors_relations if x.uuid_setor == sector_name_db.uuid]

    assert sector_name_db.active == True
    assert sector_name_2_db.active == False
    assert sector_name_db.coins_quantity == 30
    assert len(sector_name_relations) == 2
    assert len(db_sectors) == 2
    assert len(db_sectors_relations) == 2
    assert len(test_session.query(Setor).all()) == 2
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 2

    mocker.patch.object(
        sut.external_collector,
        "_collect",
        return_value=[
            {"name": "sector_name", "title": "sector_title", "num_tokens": 1, "cmc_id": 1, "symbols": ["BTC", "ETH"]},
            {
                "name": "sector_name2",
                "title": "sector_title2",
                "num_tokens": 587,
                "cmc_id": 2,
                "symbols": ["BTC", "ETH"],
            },
        ],
    )

    sut.collect(test_session)

    db_sectors = test_session.query(Setor).all()
    db_sectors_relations = test_session.query(SetorCurrencyBaseInfo).all()
    sector_name_db = db_sectors[0]
    sector_name_2_db = db_sectors[1]
    sector_name_relations = [x for x in db_sectors_relations if x.uuid_setor == sector_name_db.uuid]

    assert sector_name_db.active == False
    assert sector_name_2_db.active == True
    assert sector_name_2_db.coins_quantity == 587
    assert len(sector_name_relations) == 0
    assert len(db_sectors) == 2
    assert len(db_sectors_relations) == 2
    assert len(test_session.query(Setor).all()) == 2
    assert len(test_session.query(SetorCurrencyBaseInfo).all()) == 2
