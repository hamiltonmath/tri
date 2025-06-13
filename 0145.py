from manim import *
import numpy as np

# --- Constants for easy tuning ---
LABEL_FONT_SIZE = 48
LABEL_FONT_SIZE_SMALL = 32
DOT_RADIUS_M = 0.14
SCALE_FACTOR = 0.5
RIGHT_ANGLE_SIZE = 0.12
CIRCLE_COLOR = RED
TRIANGLE_COLOR = BLUE
BRACE_COLOR = YELLOW
HIGHLIGHT_COLOR = YELLOW
MH_LINE_COLOR = RED
HN_LINE_COLOR = BLUE
EQ_FONT_SIZE = 36
BOTTOM_FONT_SIZE = 18

class Restart(Scene):
    def construct(self):
        # Geometry points
        H = np.array([0, 0, 0])
        M = np.array([-4, 0, 0])
        L = np.array([0, 3, 0])

        # 1. Draw triangle and labels
        triangle_group, dots, labels, triangle_lines = self.draw_triangle_and_labels(H, M, L)
        dot_H, dot_M, dot_L = dots
        label_H, label_M, label_L = labels
        line_HM, line_ML, line_LH = triangle_lines

        # 2. Draw right angle mark
        right_angle_mark = self.draw_right_angle_mark(H, M, L)
        self.play(FadeIn(right_angle_mark))
        self.wait(1.2)

        # 3. Group and scale
        triangle_objects = VGroup(*triangle_group, right_angle_mark)
        self.play(triangle_objects.animate.scale(SCALE_FACTOR).move_to(ORIGIN))
        self.wait(1)

        # 4. Draw circumcircle at M with radius LM
        new_H, new_M, new_L = [dot.get_center() for dot in (dot_H, dot_M, dot_L)]
        radius = np.linalg.norm(new_L - new_M)
        circle = Circle(radius=radius, color=CIRCLE_COLOR).move_to(new_M)
        self.play(Create(circle))
        self.wait(1)

        # 5. Label sides a, b, c, c_on_mn
        label_a, label_b, label_c, label_c_on_mn = self.label_triangle_sides(new_H, new_M, new_L)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), FadeIn(label_c_on_mn))
        self.wait(1)

        # 6. Draw diameter and label T, N
        diameter, dot_T, dot_N, label_T, label_N = self.draw_diameter_and_labels(new_M, radius)
        self.play(Create(diameter), FadeIn(dot_T), FadeIn(dot_N), FadeIn(label_T), FadeIn(label_N))
        self.wait(1)

        # 7. Draw lines LT and LN, right angle at L
        line_LT = Line(new_L, dot_T.get_center(), color=WHITE)
        line_LN = Line(new_L, dot_N.get_center(), color=WHITE)
        self.play(Create(line_LT), Create(line_LN))
        self.wait(1)
        right_angle_TLN = self.draw_right_angle_mark(new_L, dot_T.get_center(), dot_N.get_center(), size=RIGHT_ANGLE_SIZE)
        self.play(FadeIn(right_angle_TLN))
        self.wait(1)

        # --- Show explanation after right angle at TLN ---
        angle_label = MathTex(r"\angle TLN", font_size=28)
        is_right = Text("is right because", font_size=24)
        reason = Text("it opens up to a semicircle", font_size=24)
        explanation = VGroup(angle_label, is_right, reason).arrange(DOWN, buff=0.15).next_to(right_angle_TLN, RIGHT, buff=0.6)
        self.play(FadeIn(explanation))
        self.wait(1.7)
        self.play(FadeOut(explanation))
        self.wait(0.2)

        # 8. LM is a radius, highlight c, fade out, repeat for TM and MN
        c_dup, brace, c_above_brace = self.mark_and_label_radius(
            new_L, new_M, dot_T.get_center(), dot_N.get_center(), label_c, dot_M.get_center(), dot_N.get_center()
        )

        # 9. Scale and arrange everything for equation
        remain_group = VGroup(
            dot_H, label_H, dot_M, label_M, dot_L, label_L,
            line_HM, line_ML, line_LH, right_angle_mark,
            label_a, label_b, label_c, label_c_on_mn,
            diameter, dot_T, dot_N, label_T, label_N,
            line_LT, line_LN, right_angle_TLN,
            c_dup, brace, c_above_brace
        )
        self.arrange_final(
            remain_group, dot_M, dot_H, dot_N, label_c_on_mn, c_above_brace, brace,
            diameter, new_H, new_M, new_L
        )

    # --- Modular methods below ---

    def draw_triangle_and_labels(self, H, M, L):
        dot_H = Dot(H, color=WHITE)
        dot_M = Dot(M, color=RED, radius=DOT_RADIUS_M)
        dot_L = Dot(L, color=WHITE)
        label_H = Text("H", font_size=LABEL_FONT_SIZE).next_to(dot_H, direction=DOWN+LEFT, buff=0.25)
        label_M = Text("M", font_size=LABEL_FONT_SIZE).next_to(dot_M, DOWN)
        label_L = Text("L", font_size=LABEL_FONT_SIZE).next_to(dot_L, UP)
        self.play(FadeIn(dot_H), FadeIn(label_H))
        self.wait(0.5)
        self.play(FadeIn(dot_M), FadeIn(label_M))
        self.wait(0.5)
        self.play(FadeIn(dot_L), FadeIn(label_L))
        self.wait(0.5)
        line_HM = Line(H, M, color=TRIANGLE_COLOR)
        line_ML = Line(M, L, color=TRIANGLE_COLOR)
        line_LH = Line(L, H, color=TRIANGLE_COLOR)
        self.play(Create(line_HM)); self.wait(0.3)
        self.play(Create(line_ML)); self.wait(0.3)
        self.play(Create(line_LH)); self.wait(0.3)
        return [dot_H, dot_M, dot_L, label_H, label_M, label_L, line_HM, line_ML, line_LH], (dot_H, dot_M, dot_L), (label_H, label_M, label_L), (line_HM, line_ML, line_LH)

    def label_triangle_sides(self, H, M, L):
        v1 = (M - H) / np.linalg.norm(M - H)
        v_LH = (H - L) / np.linalg.norm(H - L)
        v_ML = (L - M) / np.linalg.norm(L - M)
        # a
        midpoint_MH = (M + H) / 2
        label_a = MathTex("a", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_MH + 0.18 * np.array([-v1[1], v1[0], 0])
        )
        # b
        normal = np.array([-v_LH[1], v_LH[0], 0])
        midpoint_LH = (L + H) / 2
        label_b = MathTex("b", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_LH - 0.18 * normal
        )
        # c (side)
        midpoint_ML = (M + L) / 2
        label_c = MathTex("c", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_ML + 0.18 * np.array([-v_ML[1], v_ML[0], 0])
        )
        # c on MN segment (for animation)
        mn_vec = (L - M)
        mn_unit = mn_vec / np.linalg.norm(mn_vec)
        mn_center = (M + L)/2
        label_c_on_mn = MathTex("c", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            mn_center + 0.18 * np.array([-mn_unit[1], mn_unit[0], 0])
        )
        label_c_on_mn.set_z_index(3)
        return label_a, label_b, label_c, label_c_on_mn

    def draw_diameter_and_labels(self, center, radius):
        left = center + np.array([-radius, 0, 0])
        right = center + np.array([radius, 0, 0])
        diameter = Line(left, right, color=WHITE)
        dot_T = Dot(left, color=WHITE)
        dot_N = Dot(right, color=WHITE)
        label_T = Text("T", font_size=int(LABEL_FONT_SIZE * SCALE_FACTOR)).next_to(dot_T, LEFT)
        label_N = Text("N", font_size=int(LABEL_FONT_SIZE * SCALE_FACTOR)).next_to(dot_N, RIGHT)
        return diameter, dot_T, dot_N, label_T, label_N

    def draw_right_angle_mark(self, A, B, C, size=RIGHT_ANGLE_SIZE):
        v1 = (np.array(B) - np.array(A)) / np.linalg.norm(np.array(B) - np.array(A))
        v2 = (np.array(C) - np.array(A)) / np.linalg.norm(np.array(C) - np.array(A))
        p1 = np.array(A) + v1 * size
        p2 = p1 + v2 * size
        p3 = np.array(A) + v2 * size
        return Polygon(A, p1, p2, p3, color=WHITE, fill_opacity=0.7).set_fill(WHITE, opacity=0.7)

    def mark_and_label_radius(self, L, M, T, N, label_c, M_actual, N_actual):
        # LM
        lm_text = Text("LM is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(lm_text))
        self.wait(1)
        circ_c = Circle(0.26, color=HIGHLIGHT_COLOR).move_to(label_c.get_center())
        self.play(Create(circ_c)); self.wait(0.7)
        self.play(FadeOut(lm_text), FadeOut(circ_c)); self.wait(0.3)

        # TM
        tm_text = Text("TM is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(tm_text)); self.wait(1)
        tm_mid = (T + M) / 2
        circ_tm = Circle(0.24, color=HIGHLIGHT_COLOR).move_to(tm_mid)
        self.play(Create(circ_tm)); self.wait(0.7)
        c_dup = label_c.copy()
        self.play(c_dup.animate.move_to(tm_mid).scale(0.85 * circ_tm.radius / label_c.height))
        self.wait(1)
        self.play(FadeOut(tm_text)); self.wait(0.7)
        self.play(FadeOut(circ_tm)); self.wait(0.7)

        # MN
        mn_text = Text("MN is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(mn_text)); self.wait(1)
        brace = BraceBetweenPoints(M_actual, N_actual, direction=UP, color=BRACE_COLOR)
        self.play(Create(brace)); self.wait(0.7)
        c_above_brace = MathTex("c").scale(1.0).move_to(brace.get_center() + UP * 0.4)
        self.play(FadeIn(c_above_brace)); self.wait(1)
        self.play(FadeOut(mn_text)); self.wait(0.5)
        # fade out the red circle (should be the last Circle in the scene)
        for m in reversed(self.mobjects):
            if isinstance(m, Circle) and m.get_color() == CIRCLE_COLOR:
                self.play(FadeOut(m))
                self.wait(0.5)
                break
        return c_dup, brace, c_above_brace

    def arrange_final(self, remain_group, dot_M, dot_H, dot_N, label_c_on_mn, c_above_brace, brace, diameter, new_H, new_M, new_L):
        frame_width = config.frame_width if hasattr(config, "frame_width") else 14.222
        frame_height = config.frame_height if hasattr(config, "frame_height") else 8.0
        target_width = frame_width * 0.65
        scale_needed = target_width / remain_group.width
        up_shift = frame_height * 0.25
        self.play(remain_group.animate.scale(scale_needed).move_to(UP * up_shift), run_time=1)
        self.wait(1)

        # (1) Place equation in bottom half (MH + HN = MN, all white initially)
        eq_mh = MathTex("MH", font_size=EQ_FONT_SIZE).move_to([-2.5, -2, 0])
        eq_plus = Text("+", font_size=EQ_FONT_SIZE).next_to(eq_mh, RIGHT, buff=0.16)
        eq_hn = MathTex("HN", font_size=EQ_FONT_SIZE).next_to(eq_plus, RIGHT, buff=0.16)
        eq_eq = Text("=", font_size=EQ_FONT_SIZE).next_to(eq_hn, RIGHT, buff=0.16)
        eq_mn = MathTex("MN", font_size=EQ_FONT_SIZE).next_to(eq_eq, RIGHT, buff=0.16)
        eq_group = VGroup(eq_mh, eq_plus, eq_hn, eq_eq, eq_mn)
        self.play(FadeIn(eq_group))
        self.wait(0.5)

        # (2) MH on equation turns blue
        self.play(eq_mh.animate.set_color(HN_LINE_COLOR))
        self.wait(0.2)

        # (3) MH on diagram highlighted blue
        mh_line = Line(dot_M.get_center(), dot_H.get_center(), color=HN_LINE_COLOR, stroke_width=10)
        self.play(Create(mh_line))
        self.wait(0.2)

        # (4) plus already present

        # (5) HN on equation turns red
        self.play(eq_hn.animate.set_color(MH_LINE_COLOR))
        self.wait(0.2)

        # (6) HN on diagram highlighted red
        hn_line = Line(dot_H.get_center(), dot_N.get_center(), color=MH_LINE_COLOR, stroke_width=10)
        self.play(Create(hn_line))
        self.wait(0.2)

        # (7) = sign present

        # (8) MN on equation stays white, already present

        # (9) Circle c on diagram at MN (label_c_on_mn is the c on MN)
        circ_c = Circle(0.32, color=HIGHLIGHT_COLOR).move_to(label_c_on_mn.get_center())
        self.play(FadeIn(label_c_on_mn))
        self.play(Create(circ_c))
        self.wait(0.3)

        # (10) Morph equation MH to a
        eq_a = MathTex("a", font_size=EQ_FONT_SIZE).set_color(HN_LINE_COLOR).move_to(eq_mh.get_center())
        self.play(Transform(eq_mh, eq_a))
        self.wait(0.2)

        # (11) Morph equation MN to c (move label_c_on_mn to equation)
        label_c_on_mn.save_state()
        self.play(label_c_on_mn.animate.move_to(eq_mn.get_center()))
        self.wait(0.2)
        self.play(Transform(eq_mn, label_c_on_mn))
        self.wait(0.2)

        # (12) "Solve": morph to HN = c - a
        eq_hn_new = MathTex("HN", font_size=EQ_FONT_SIZE).set_color(MH_LINE_COLOR)
        eq_eq_new = Text("=", font_size=EQ_FONT_SIZE)
        eq_c_new = eq_mn  # Now eq_mn IS label_c_on_mn, already on equation
        eq_minus = Text("-", font_size=EQ_FONT_SIZE)
        eq_a_new = eq_a.copy()
        eq_group_new = VGroup(eq_hn_new, eq_eq_new, eq_c_new, eq_minus, eq_a_new).arrange(RIGHT, buff=0.13)
        eq_group_new.move_to(eq_group.get_center())
        self.play(Transform(eq_group, eq_group_new))
        self.wait(0.7)

        # (13) Place c-a label on HN, tightly below the line, reduced spacing
        label_c_minus_a = MathTex("c-a", font_size=LABEL_FONT_SIZE_SMALL, color=HN_LINE_COLOR)
        # Place tightly below the HN line
        hn_vec = dot_N.get_center() - dot_H.get_center()
        perp = np.array([-hn_vec[1], hn_vec[0], 0])
        perp = perp / np.linalg.norm(perp)
        label_c_minus_a.move_to(hn_line.get_center() - 0.27*perp - 0.03*hn_vec/np.linalg.norm(hn_vec))
        self.play(FadeIn(label_c_minus_a))
        self.wait(0.3)

        # (14) MH and HN diagram lines turn white
        self.play(mh_line.animate.set_color(WHITE), hn_line.animate.set_color(WHITE))
        self.wait(0.2)

        # (15) Uncircle c on diagram (circle is no longer needed where c was)
        self.play(FadeOut(circ_c))
        self.wait(0.2)

        # (16) Fade out c that was circled (i.e., the c that was on MN and now in equation)
        self.play(FadeOut(eq_c_new))
        self.wait(0.2)

        # (17) Fade out the bracket
        self.play(FadeOut(brace))
        self.wait(0.3)