shader_type canvas_item;

// 王小桃卡框：左粉右蓝的浅色渐变。
// 用原版卡框的亮度保留凹槽/高光/黑描边，只替换色相与饱和度。
uniform vec3 pink : source_color = vec3(0.96, 0.75, 0.84);
uniform vec3 blue : source_color = vec3(0.74, 0.84, 0.98);
uniform float strength : hint_range(0.0, 1.0) = 1.0;
// %Frame 用的是 AtlasTexture；shader 里的 UV 是整张图集的归一化坐标。
// 由 C# 按 AtlasTexture.Region/Atlas.GetSize() 写入，才能得到卡框自己的 0..1。
uniform vec2 uv_offset = vec2(0.0, 0.0);
uniform vec2 uv_scale = vec2(1.0, 1.0);

varying vec4 modulate_color;

void vertex() {
    modulate_color = COLOR;
}

void fragment() {
    vec4 col = texture(TEXTURE, UV);
    float l = dot(col.rgb, vec3(0.299, 0.587, 0.114));
    vec2 card_uv = (UV - uv_offset) / max(uv_scale, vec2(0.0001, 0.0001));
    vec3 gradient = mix(pink, blue, clamp(card_uv.x, 0.0, 1.0));

    // 外框直接给足亮度的粉蓝，不再保留原图暗红底的亮度；
    // 只把接近纯黑的描边/缝隙留在深色，避免整圈糊成一块。
    float outline = smoothstep(0.0, 0.035, l);
    float shade = 0.82 + 0.18 * smoothstep(0.08, 0.55, l);
    vec3 tinted = mix(vec3(0.02, 0.015, 0.03), gradient * shade, outline);

    // 正文区保持深色底 + 少量渐变；底部外框不压暗。
    float body = smoothstep(0.30, 0.42, card_uv.y)
        * (1.0 - smoothstep(0.93, 0.97, card_uv.y))
        * smoothstep(0.03, 0.08, card_uv.x)
        * smoothstep(0.03, 0.08, 1.0 - card_uv.x);
    float borderMix = smoothstep(0.15, 0.50, l);
    vec3 bodyTint = vec3(0.115, 0.10, 0.145) + gradient * (0.18 + 0.22 * borderMix);
    tinted = mix(tinted, bodyTint, body);

    col.rgb = mix(col.rgb, tinted, strength);
    // 外框靠里的半透明像素会在卡面底色上显得发灰/透；彩色区域至少保留 92% 不透明度，
    // 纯黑描边和中央镂空仍沿用原 alpha。
    col.a = max(col.a, outline * 0.92);
    COLOR = col;
    COLOR *= modulate_color;
}
