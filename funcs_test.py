import pytest

from funcs import zmod, mod, fact, comb

def test_zmod():
	assert zmod(-3,3) == 0
	assert zmod(-2,3) == 1
	assert zmod(-1,3) == 2
	assert zmod(0,3) == 0
	assert zmod(1,3) == 1
	assert zmod(2,3) == 2
	assert zmod(3,3) == 0

def test_mod():
	assert mod(-3,3) == 3
	assert mod(-2,3) == 1
	assert mod(-1,3) == 2
	assert mod(0,3) == 3
	assert mod(1,3) == 1
	assert mod(2,3) == 2
	assert mod(3,3) == 3

def test_fact():
	assert fact(0) == 1
	assert fact(1) == 1
	assert fact(2) == 2
	assert fact(3) == 6
	assert fact(4) == 24
	assert fact(5) == 120

def test_comb():
	"""n = 1"""
	assert comb(1, 1) == 1
	"""n = 2"""
	assert comb(2, 0) == 1
	assert comb(2, 1) == 2
	assert comb(2, 2) == 1
	"""n = 4"""
	assert comb(4, 0) == 1
	assert comb(4, 1) == 4
	assert comb(4, 2) == 6
	assert comb(4, 3) == 4
	assert comb(4, 4) == 1
	"""High value symmetric checks"""
	for k in range(1001):
		assert comb(1000, k) == comb(1000, 1000 - k)