import pytest, time
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)
from brownie import network


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    print("Lottery is open!")
    print("Players joining...")
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    print("Players have joined!")
    fund_with_link(lottery)
    print("Closing lottery...")
    lottery.endLottery({"from": account})
    print("Lottery closed!")
    print("Getting winner...")
    print("(takes 3-5 mins)")
    time.sleep(300)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
