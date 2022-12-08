from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


# 도메인 예외 발생
class OutOfStock(Exception):
    pass


# def allocate(line: OrderLine, batches:List[Batch]) -> str:
#     batch = next(
#         b for b in sorted(batches) if b.can_allocate(line)
#     )
#     batch.allocate(line)
#     return batch.reference

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")

# 값 객체(Value Object)
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

# 엔티티(Entity)
class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        # self.available_quantity = qty
        self._purchased_quantity = qty
        self._allocations = set() # type: Set[OrderLine] # 중복 X
    
    def __repr__(self):
        return f"<Batch {self.reference}>"
    
    # 정체성 동등성을 위해
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
    
    
    # sorted() 작동을 가능하게 해줌
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line) # 주문 추가
        
    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line) # 주문 제거
    
    # 총 재고
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    # 총 재고 - 주문
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    
    # 할당 체크
    def can_allocate(self, line: OrderLine) -> bool:
        # 같은 제품 && 재고 > 주문
        return self.sku == line.sku and self.available_quantity >= line.qty
    

