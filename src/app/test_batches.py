from datetime import date
from model import Batch, OrderLine

# 할당 테스트
def test_allocating_to_a_batch_reduces_the_available_quantity():
    # 재고 현황
    batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=date.today())
    # 주문 내용
    line = OrderLine('order-ref', 'SMALL-TABLE', 2)
    # 할당
    batch.allocate(line)
    
    # 결과 테스트
    assert batch.available_quantity == 18

# 재고 - 주문을 바로 할 수 있는 함수 정의
def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch('batch-001', sku, batch_qty, eta=date.today())
        , OrderLine('order-123', sku, line_qty)
    )


# 재고 < 주문
def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line('ELEGANT-LAMP', 20, 2)
    
    assert large_batch.can_allocate(small_line)

# 재고 = 주문
def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line('ELEGANT-LAMP', 2, 2)
    
    assert batch.can_allocate(line)

# 재고 > 주문
def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line('ELEGANT-LAMP', 2, 20)
    
    assert small_batch.can_allocate(large_line) is False
    
# 제품 != 제품
def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch-001', 'CAT-LAMP', 100, eta=None)
    different_sku_line = OrderLine('order-123', 'DOG-CHAIR', 10)
    
    assert batch.can_allocate(different_sku_line) is False

# 주문 취소시 재고
def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

# Set 때문에 중복X -> 같은 주문이 여러번 들어와도 재고변화X
def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18
    

def test_deallocate():
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20