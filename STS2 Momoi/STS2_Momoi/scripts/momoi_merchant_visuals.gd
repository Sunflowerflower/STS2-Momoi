extends Sprite2D

## 商店（merchant）的 relaxed 交替动画。
## 参考 AEP comp「12交替频率」：一个完整循环 2.29157118453398s，
## 两张图各占一半 = 1.1457856s。改 speed 可整体调速。
## 注意：这个值与 STS2 MomoiCharacter.cs 里的 RelaxedHalfCycleSeconds 保持一致。

const FRAME_A := preload("res://STS2_Momoi/images/characters/cue/relaxed.png")
const FRAME_B := preload("res://STS2_Momoi/images/characters/cue/relaxed_2.png")

@export var speed: float = 1.0
@export var half_cycle_seconds: float = 1.1457856

var _elapsed := 0.0
var _frame := 0

func _ready() -> void:
	texture = FRAME_A
	_elapsed = 0.0
	_frame = 0

func _process(delta: float) -> void:
	var half := half_cycle_seconds / maxf(speed, 0.01)
	_elapsed += delta
	while _elapsed >= half:
		_elapsed -= half
		_frame = 1 - _frame
		texture = FRAME_A if _frame == 0 else FRAME_B
