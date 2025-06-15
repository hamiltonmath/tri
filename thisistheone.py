from manim import *
import numpy as np

LABEL_FONT_SIZE = 48
LABEL_FONT_SIZE_SMALL = 32
DOT_RADIUS_M = 0.14
SCALE_FACTOR = 0.5
RIGHT_ANGLE_SIZE = 0.12
INITIAL_RIGHT_ANGLE_SIZE = 0.28
CIRCLE_COLOR = RED
TRIANGLE_COLOR = BLUE
BRACE_COLOR = YELLOW
HIGHLIGHT_COLOR = YELLOW
MH_LINE_COLOR = RED
HN_LINE_COLOR = BLUE
HIGHLIGHT_GREEN = GREEN
EQ_FONT_SIZE = 36
BOTTOM_FONT_SIZE = 18

class Restart(Scene):
    def construct(self):
        H = np.array([0, 0, 0])
        M = np.array([-4, 0, 0])
        L = np.array([0, 3, 0])

        triangle_group, dots, labels, triangle_lines = self.draw_triangle_and_labels(H, M, L)
        dot_H, dot_M, dot_L = dots
        label_H, label_M, label_L = labels
        line_HM, line_ML, line_LH = triangle_lines

        right_angle_mark = self.draw_right_angle_mark(H, M, L, size=INITIAL_RIGHT_ANGLE_SIZE)
        self.play(FadeIn(right_angle_mark))
        self.wait(1.2)

        triangle_objects = VGroup(*triangle_group, right_angle_mark)
        self.play(triangle_objects.animate.scale(SCALE_FACTOR).move_to(ORIGIN))
        self.wait(1)

        new_H, new_M, new_L = [dot.get_center() for dot in (dot_H, dot_M, dot_L)]
        radius = np.linalg.norm(new_L - new_M)
        circle = Circle(radius=radius, color=CIRCLE_COLOR).move_to(new_M)
        self.play(Create(circle))
        self.wait(1)

        label_a, label_b, label_c, label_c_on_mn = self.label_triangle_sides(new_H, new_M, new_L)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), FadeIn(label_c_on_mn))
        self.wait(1)

        diameter, dot_T, dot_N, label_T, label_N = self.draw_diameter_and_labels(new_M, radius)
        self.play(Create(diameter), FadeIn(dot_T), FadeIn(dot_N), FadeIn(label_T), FadeIn(label_N))
        self.wait(1)

        line_LT = Line(new_L, dot_T.get_center(), color=WHITE)
        line_LN = Line(new_L, dot_N.get_center(), color=WHITE)
        self.play(Create(line_LT), Create(line_LN))
        self.wait(1)
        right_angle_TLN = self.draw_right_angle_mark(new_L, dot_T.get_center(), dot_N.get_center(), size=RIGHT_ANGLE_SIZE)
        self.play(FadeIn(right_angle_TLN))
        self.wait(1)

        explanation_line1 = VGroup(
            MathTex(r"\angle TLN", font_size=28),
            Text("is right because", font_size=24)
        ).arrange(RIGHT, buff=0.15)
        explanation_line2 = Text("it opens up to a semicircle.", font_size=24)
        explanation = VGroup(explanation_line1, explanation_line2).arrange(DOWN, buff=0.15).next_to(right_angle_TLN, UP+RIGHT, buff=0.8)
        self.play(FadeIn(explanation))
        self.wait(1.7)
        self.play(FadeOut(explanation))
        self.wait(0.2)

        c_dup, brace, c_above_brace = self.mark_and_label_radius(
            new_L, new_M, dot_T.get_center(), dot_N.get_center(), label_c, dot_M.get_center(), dot_N.get_center()
        )

        remain_group = VGroup(
            dot_H, label_H, dot_M, label_M, dot_L, label_L,
            line_HM, line_ML, line_LH, right_angle_mark,
            label_a, label_b, label_c, label_c_on_mn,
            diameter, dot_T, dot_N, label_T, label_N,
            line_LT, line_LN, right_angle_TLN,
            c_dup, brace, c_above_brace
        )

        self.arrange_final(
            remain_group, dot_M, dot_H, dot_N, label_a, label_c_on_mn, c_above_brace, brace,
            diameter, new_H, new_M, new_L, dot_L, dot_N, line_LN, label_a, line_HM, dot_T,
            label_c, c_dup, line_ML, dot_T, dot_L, dot_M, label_c
        )

        # --- Fade out the "According to..." lines ---
        # Use the direct variable for the VGroup created below
        everything = VGroup(remain_group)
        diagram_bottom = everything.get_bottom()

        exterior_text = VGroup(
            Text("According to the Exterior Angle Theorem...", font_size=LABEL_FONT_SIZE_SMALL),
            Text("They must have the same value and add to 2x.", font_size=LABEL_FONT_SIZE_SMALL),
            Text("So they must both be x.", font_size=LABEL_FONT_SIZE_SMALL)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        exterior_text.move_to(diagram_bottom + DOWN * 0.7)
        self.add(exterior_text)
        self.play(FadeIn(exterior_text))
        self.wait(1.8)
        self.play(FadeOut(exterior_text))
        self.wait(0.4)

        # ---- Begin new animation for TM + MH = TH ----

        T_pos = dot_T.get_center()
        H_pos = dot_H.get_center()
        M_pos = dot_M.get_center()

        # 1. Draw brace under dot T and dot H (across T and H), in yellow
        brace_th = BraceBetweenPoints(T_pos, H_pos, direction=DOWN, color=BRACE_COLOR)
        self.play(Create(brace_th))
        self.wait(0.4)

        # 2. TM on the diagram turns blue
        line_TM = Line(T_pos, M_pos, color=HN_LINE_COLOR, stroke_width=10)
        self.play(Create(line_TM))
        self.wait(0.2)

        # 3. MH on the diagram turns red
        line_MH = Line(M_pos, H_pos, color=MH_LINE_COLOR, stroke_width=10)
        self.play(Create(line_MH))
        self.wait(0.2)

        # 4. Equation at bottom: TM (blue) + (white) MH (red) = (white) TH (white)
        eq_tm = MathTex("TM", font_size=EQ_FONT_SIZE, color=HN_LINE_COLOR)
        eq_plus = Text("+", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_mh = MathTex("MH", font_size=EQ_FONT_SIZE, color=MH_LINE_COLOR)
        eq_eq = Text("=", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_th = MathTex("TH", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_group = VGroup(eq_tm, eq_plus, eq_mh, eq_eq, eq_th).arrange(RIGHT, buff=0.18)
        eq_group.next_to(brace_th, DOWN, buff=1.1)
        self.play(FadeIn(eq_group))
        self.wait(0.4)

        # 5. Animate the "c" and "a" from the diagram to the equation (leaving nothing)
        label_c.generate_target()
        label_c.target.move_to(eq_tm.get_center())
        label_c.target.set_color(HN_LINE_COLOR)
        label_c.target.scale(EQ_FONT_SIZE/LABEL_FONT_SIZE_SMALL)
        label_a.generate_target()
        label_a.target.move_to(eq_mh.get_center())
        label_a.target.set_color(MH_LINE_COLOR)
        label_a.target.scale(EQ_FONT_SIZE/LABEL_FONT_SIZE_SMALL)
        self.play(
            FadeOut(eq_tm),
            FadeOut(eq_mh),
            MoveToTarget(label_c),
            MoveToTarget(label_a)
        )
        eq_group.submobjects[0] = label_c
        eq_group.submobjects[2] = label_a
        self.wait(0.4)

        # 6. The letter M on the diagram disappears
        self.play(FadeOut(label_M))
        self.wait(0.2)
        # 7. The dot at M disappears
        self.play(FadeOut(dot_M))
        self.wait(0.2)

        # 8. Both TM and MH lines turn white
        self.play(
            line_TM.animate.set_color(WHITE),
            line_MH.animate.set_color(WHITE)
        )
        self.wait(0.2)

        # 9. (Optional) Equation disappears
        self.play(FadeOut(eq_group))
        self.wait(0.3)

    # --- Helper methods (unchanged) below here ---
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
        midpoint_MH = (M + H) / 2
        label_a = MathTex("a", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_MH + 0.18 * np.array([-v1[1], v1[0], 0])
        )
        normal = np.array([-v_LH[1], v_LH[0], 0])
        midpoint_LH = (L + H) / 2
        label_b = MathTex("b", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_LH - 0.18 * normal
        )
        midpoint_ML = (M + L) / 2
        label_c = MathTex("c", font_size=LABEL_FONT_SIZE_SMALL).move_to(
            midpoint_ML + 0.18 * np.array([-v_ML[1], v_ML[0], 0])
        )
        mn_vec = (L - M)
        mn_unit = mn_vec / np.linalg.norm(L - M)
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
        lm_text = Text("LM is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(lm_text))
        self.wait(1)
        circ_c = Circle(0.26, color=HIGHLIGHT_COLOR).move_to(label_c.get_center())
        self.play(Create(circ_c)); self.wait(0.7)
        self.play(FadeOut(lm_text), FadeOut(circ_c)); self.wait(0.3)

        tm_text = Text("TM is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(tm_text)); self.wait(1)

        mt_vec = T - M
        perp_mt = np.array([-mt_vec[1], mt_vec[0], 0])
        perp_mt /= np.linalg.norm(perp_mt)
        offset = 0.18 * perp_mt
        tm_mid = (T + M) / 2
        c_on_mt_pos = tm_mid + offset
        c_dup = MathTex("c", font_size=LABEL_FONT_SIZE_SMALL).move_to(c_on_mt_pos)
        self.add(c_dup)
        self.wait(1)
        self.play(FadeOut(tm_text))
        self.wait(0.7)

        mn_text = Text("and MN is a radius.", font_size=LABEL_FONT_SIZE_SMALL).move_to(L + np.array([2.8, 1.0, 0]))
        self.play(FadeIn(mn_text)); self.wait(1)
        brace = BraceBetweenPoints(M_actual, N_actual, direction=UP, color=BRACE_COLOR)
        self.play(Create(brace)); self.wait(0.7)
        lm_mid = (L + M) / 2
        c_brace = label_c.copy().move_to(lm_mid)
        self.play(c_brace.animate.move_to(brace.get_center() + UP * 0.4))
        self.wait(1)
        self.play(FadeOut(mn_text)); self.wait(0.5)
        for m in reversed(self.mobjects):
            if isinstance(m, Circle) and m.get_color() == CIRCLE_COLOR:
                self.play(FadeOut(m))
                self.wait(0.5)
                break
        return c_dup, brace, c_brace

    def arrange_final(
        self, remain_group, dot_M, dot_H, dot_N, label_a, label_c_on_mn, c_above_brace, brace,
        diameter, new_H, new_M, new_L, dot_L, dot_N_real, line_LN, label_a_obj, line_HM, dot_T,
        label_c, c_dup, line_ML, dot_T_obj, dot_L_obj, dot_M_obj, label_c_lm
    ):
        frame_width = config.frame_width if hasattr(config, "frame_width") else 14.222
        frame_height = config.frame_height if hasattr(config, "frame_height") else 8.0
        target_width = frame_width * 0.65
        scale_needed = target_width / remain_group.width
        up_shift = frame_height * 0.25
        self.play(remain_group.animate.scale(scale_needed).move_to(UP * up_shift), run_time=1)
        self.wait(1)

        eq_mh = MathTex("MH", font_size=EQ_FONT_SIZE, color=HN_LINE_COLOR)
        eq_plus = Text("+", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_hn = MathTex("HN", font_size=EQ_FONT_SIZE, color=MH_LINE_COLOR)
        eq_eq = Text("=", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_mn = MathTex("MN", font_size=EQ_FONT_SIZE, color=WHITE)
        eq_group = VGroup(eq_mh, eq_plus, eq_hn, eq_eq, eq_mn).arrange(RIGHT, buff=0.18)
        eq_group.move_to([0, -0.4, 0])
        self.play(FadeIn(eq_group))
        self.wait(0.5)

        M_pos = dot_M.get_center()
        H_pos = dot_H.get_center()
        N_pos = dot_N.get_center()
        mn_line = Line(M_pos, N_pos, color=WHITE, stroke_width=6)
        self.add(mn_line)
        mh_line = Line(M_pos, H_pos, color=HN_LINE_COLOR, stroke_width=10)
        hn_line = Line(H_pos, N_pos, color=MH_LINE_COLOR, stroke_width=10)
        self.play(Create(mh_line), Create(hn_line))
        self.wait(0.2)

        label_a_fly = label_a.copy().scale(1.1).set_color(HN_LINE_COLOR)
        label_a_fly.save_state()
        label_a_fly.generate_target()
        label_a_fly.target.move_to(eq_mh)
        self.play(MoveToTarget(label_a_fly), FadeOut(eq_mh))
        self.wait(0.2)

        circ_c = Circle(0.32, color=HIGHLIGHT_COLOR).move_to(c_above_brace.get_center())
        self.play(Create(circ_c))
        self.wait(0.3)

        self.play(FadeOut(eq_mn))
        self.play(FadeOut(circ_c))
        c_above_brace.save_state()
        self.play(c_above_brace.animate.move_to(eq_mn.get_center()))
        self.wait(0.2)

        self.play(FadeOut(brace))
        self.wait(0.3)

        self.remove(eq_group, eq_mh, eq_mn, eq_plus, eq_hn, eq_eq)

        equation_a = label_a_fly
        equation_plus = Text("+", font_size=EQ_FONT_SIZE, color=WHITE)
        equation_hn = MathTex("HN", font_size=EQ_FONT_SIZE, color=MH_LINE_COLOR)
        equation_eq = Text("=", font_size=EQ_FONT_SIZE, color=WHITE)
        equation_c = c_above_brace
        equation_group = VGroup(equation_a, equation_plus, equation_hn, equation_eq, equation_c).arrange(RIGHT, buff=0.18)
        equation_group.move_to([0, -0.4, 0])
        self.add(equation_group)
        self.wait(0.6)

        hn_eq = MathTex("HN", "=", "c - a", font_size=LABEL_FONT_SIZE_SMALL)
        hn_eq[2].set_color(HIGHLIGHT_COLOR)
        hn_eq.next_to(equation_group, DOWN, buff=0.3)
        self.play(FadeIn(hn_eq))
        self.wait(0.7)

        hn_midpoint = (dot_H.get_center() + dot_N_real.get_center()) / 2
        hn_vec = dot_N_real.get_center() - dot_H.get_center()
        perp = np.array([-hn_vec[1], hn_vec[0], 0])
        perp = perp / np.linalg.norm(perp)
        diagram_offset = -0.28 * perp
        c_minus_a_label = MathTex("c\\!-\!a", font_size=LABEL_FONT_SIZE_SMALL, color=WHITE)
        c_minus_a_label.move_to(hn_midpoint + diagram_offset)
        self.play(FadeIn(c_minus_a_label))
        self.wait(1.0)

        self.play(
            equation_a.animate.set_color(WHITE),
            equation_hn.animate.set_color(WHITE)
        )
        self.wait(0.6)

        self.play(FadeOut(line_HM))
        self.wait(0.5)

        self.play(mh_line.animate.set_color(WHITE))
        self.wait(0.2)

        self.play(hn_line.animate.set_color(WHITE))
        self.wait(0.2)

        self.play(FadeOut(equation_group), FadeOut(hn_eq))
        self.wait(0.5)

        everything = VGroup(remain_group)
        diagram_bottom = everything.get_bottom()

        # Place "Let's let ..." line (fixed: LMH instead of LHM)
        instruction = MathTex(
            r"\text{Let's let}\ \angle LMH = 2x", font_size=LABEL_FONT_SIZE_SMALL
        ).next_to(diagram_bottom, DOWN, buff=0.7)
        self.play(Write(instruction))
        self.wait(0.8)

        # Place 2x label in the diagram above M, below L, 1/7 of the way to L vertically, 1/7 to N horizontally
        M_pos = dot_M_obj.get_center()
        N_pos = dot_N_real.get_center()
        L_pos = dot_L_obj.get_center()
        T_pos = dot_T_obj.get_center()
        vertical_vector = L_pos - M_pos
        horizontal_vector = N_pos - M_pos
        custom_pos = M_pos + (1/7) * vertical_vector + (1/7) * horizontal_vector
        two_x_label = MathTex("2x", font_size=LABEL_FONT_SIZE_SMALL, color=YELLOW).move_to(custom_pos)
        self.play(FadeIn(two_x_label))
        self.wait(1.0)

        self.play(FadeOut(instruction))
        self.wait(0.5)

        # Highlight TL, LM, MT in green
        tl_line = Line(T_pos, L_pos, color=HIGHLIGHT_GREEN, stroke_width=10)
        lm_line = Line(L_pos, M_pos, color=HIGHLIGHT_GREEN, stroke_width=10)
        mt_line = Line(M_pos, T_pos, color=HIGHLIGHT_GREEN, stroke_width=10)
        self.play(Create(tl_line), Create(lm_line), Create(mt_line))
        self.wait(0.3)

        two_x_label_color = YELLOW

        # q1: (vertically) 1/7 from T to L, (horizontally) 1/4 from T to M
        q1_pos = T_pos + (1/7) * (L_pos - T_pos) + (1/4) * (M_pos - T_pos)
        q1 = MathTex("?", font_size=LABEL_FONT_SIZE_SMALL, color=two_x_label_color).move_to(q1_pos)
        q1.name = "q_question1"

        # q2: vertically 3/5 from M to L, horizontally at the midpoint of LM, then slightly higher and to the right
        vec_ML = L_pos - M_pos
        midpoint = (M_pos + L_pos) / 2
        q2_base = M_pos + (3/5) * vec_ML
        q2_pos = np.array(q2_base)
        q2_pos[0] = midpoint[0]
        shift = 0.10 * vec_ML
        q2_pos = q2_pos + shift
        q2 = MathTex("?", font_size=LABEL_FONT_SIZE_SMALL, color=two_x_label_color).move_to(q2_pos)
        q2.name = "q_question2"

        # Isosceles/theorem lines
        isosceles_text = MathTex(
            r"\triangle TLM\ \text{ is isosceles because } \overline{TM} \cong \overline{LM}.",
            font_size=LABEL_FONT_SIZE_SMALL, color=WHITE
        ).move_to(diagram_bottom + DOWN * 0.7)
        self.play(Write(isosceles_text))
        self.wait(0.8)

        theorem_text = MathTex(
            r"\text{According to the isosceles triangle theorem,}\ "
            r"\angle T \cong \angle TLM.",
            font_size=LABEL_FONT_SIZE_SMALL, color=WHITE
        ).next_to(isosceles_text, DOWN, buff=0.5)
        self.play(Write(theorem_text))
        self.wait(1.0)

        # Now show the question marks
        self.play(FadeIn(q1), FadeIn(q2))
        self.wait(1.2)

        # Fade out both lines simultaneously
        self.play(FadeOut(isosceles_text), FadeOut(theorem_text))
        self.wait(0.5)

        # Exterior Angle Theorem text
        exterior_text = VGroup(
            Text("According to the Exterior Angle Theorem...", font_size=LABEL_FONT_SIZE_SMALL),
            Text("They must have the same value and add to 2x.", font_size=LABEL_FONT_SIZE_SMALL),
            Text("So they must both be x.", font_size=LABEL_FONT_SIZE_SMALL)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        exterior_text.move_to(diagram_bottom + DOWN * 0.7)
        self.play(FadeIn(exterior_text))
        self.wait(1.8)

        # Morph both question marks to x's (use MathTex for both)
        x1 = MathTex("x", font_size=LABEL_FONT_SIZE_SMALL, color=two_x_label_color).move_to(q1.get_center())
        x2 = MathTex("x", font_size=LABEL_FONT_SIZE_SMALL, color=two_x_label_color).move_to(q2.get_center())
        self.play(Transform(q1, x1), Transform(q2, x2))
        self.wait(1.0)

        # Fade out LM (green), LM (triangle), c on LM, q2, and 2x (c label is NOT colored green)
        self.play(
            FadeOut(lm_line),      # Green LM segment
            FadeOut(line_ML),      # Triangle's original LM segment (blue)
            FadeOut(label_c),      # c label on LM (never colored green)
            FadeOut(q2),           # x at q2
            FadeOut(two_x_label),  # 2x label
            FadeOut(label_c_on_mn)
        )
        self.wait(0.4)