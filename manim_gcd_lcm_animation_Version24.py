from manim import *

class GCDLCMAnimation(Scene):
    def prime_factors(self, n):
        i = 2
        factors = []
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return factors

    def construct(self):
        FONT_SIZE = 24

        x, y = 9,15
        x_factors = self.prime_factors(x)
        y_factors = self.prime_factors(y)

        COMMON_COLOR = YELLOW
        X_COLOR = BLUE
        Y_COLOR = GREEN
        LCM_COLOR = ORANGE

        offset = 2.5

        x_num = MathTex(str(x), color=X_COLOR, font_size=FONT_SIZE).move_to(UP * 1.7 + LEFT * offset)
        y_num = MathTex(str(y), color=Y_COLOR, font_size=FONT_SIZE).move_to(UP * 1.7 + RIGHT * offset)
        x_underline = Underline(x_num)
        y_underline = Underline(y_num)
        self.play(Write(x_num), Write(y_num), Create(x_underline), Create(y_underline))

        x_factors_tex = MathTex(*[f"({n})" for n in x_factors], color=X_COLOR, font_size=FONT_SIZE).next_to(x_num, DOWN)
        y_factors_tex = MathTex(*[f"({n})" for n in y_factors], color=Y_COLOR, font_size=FONT_SIZE).next_to(y_num, DOWN)
        self.play(FadeIn(x_factors_tex), FadeIn(y_factors_tex))

        gcf_label = MathTex("\\underline{\\mathrm{GCF}}", font_size=FONT_SIZE).move_to(DOWN * 1.7 + LEFT * offset)
        lcm_label = MathTex("\\underline{\\mathrm{LCM}}", font_size=FONT_SIZE).move_to(DOWN * 1.7 + RIGHT * offset)

        gcf_start = gcf_label.get_left() + DOWN * 0.8 + RIGHT * 0.1
        lcm_start = lcm_label.get_left() + DOWN * 0.8 + RIGHT * 0.1

        gcf_val = MathTex("(1)", color=COMMON_COLOR, font_size=FONT_SIZE).move_to(gcf_start, aligned_edge=LEFT)
        lcm_val = MathTex("(1)", color=LCM_COLOR, font_size=FONT_SIZE).move_to(lcm_start, aligned_edge=LEFT)
        self.play(Write(gcf_label), Write(lcm_label), Write(gcf_val), Write(lcm_val))

        x_factors_list = list(x_factors)
        y_factors_list = list(y_factors)
        x_objs = [x_factors_tex[i] for i in range(len(x_factors_list))]
        y_objs = [y_factors_tex[i] for i in range(len(y_factors_list))]
        used_x = [False] * len(x_factors_list)
        used_y = [False] * len(y_factors_list)
        gcf_terms = ["(1)"]
        lcm_terms = ["(1)"]

        # Common factors animation
        for i, xf in enumerate(x_factors_list):
            for j, yf in enumerate(y_factors_list):
                if xf == yf and not used_x[i] and not used_y[j]:
                    self.play(
                        x_objs[i].animate.set_color(COMMON_COLOR),
                        y_objs[j].animate.set_color(COMMON_COLOR)
                    )
                    self.wait(0.1)
                    combo_point = ORIGIN + UP*0.3
                    x_copy = x_objs[i].copy()
                    y_copy = y_objs[j].copy()
                    self.play(
                        x_copy.animate.move_to(combo_point),
                        y_copy.animate.move_to(combo_point),
                        run_time=0.7
                    )
                    combined = MathTex(f"({xf})", color=COMMON_COLOR, font_size=FONT_SIZE).move_to(combo_point)
                    self.play(
                        FadeOut(x_copy),
                        FadeOut(y_copy),
                        FadeIn(combined)
                    )
                    self.wait(0.1)
                    gcf_target = gcf_start + RIGHT * (len(gcf_terms)) * 1.1
                    lcm_target = lcm_start + RIGHT * (len(lcm_terms)) * 1.1
                    combined_gcf = combined.copy().set_color(COMMON_COLOR)
                    combined_lcm = combined.copy().set_color(LCM_COLOR)
                    self.play(
                        FadeOut(combined),
                        combined_gcf.animate.move_to(gcf_target, aligned_edge=LEFT),
                        combined_lcm.animate.move_to(lcm_target, aligned_edge=LEFT),
                        FadeOut(x_objs[i]), FadeOut(y_objs[j])
                    )
                    self.wait(1.0)
                    gcf_terms.append(f"({xf})")
                    lcm_terms.append(f"({xf})")
                    gcf_val_new = MathTex(" \\cdot ".join(gcf_terms), color=COMMON_COLOR, font_size=FONT_SIZE).move_to(gcf_start, aligned_edge=LEFT)
                    lcm_val_new = MathTex(" \\cdot ".join(lcm_terms), color=LCM_COLOR, font_size=FONT_SIZE).move_to(lcm_start, aligned_edge=LEFT)
                    self.play(
                        FadeOut(combined_gcf),
                        FadeOut(combined_lcm),
                        Transform(gcf_val, gcf_val_new),
                        Transform(lcm_val, lcm_val_new)
                    )
                    self.wait(0.1)
                    used_x[i] = True
                    used_y[j] = True
                    break

        # Leftover factors animated to LCM
        for i, used in enumerate(used_x):
            if not used:
                obj = x_objs[i]
                copy = obj.copy().set_color(LCM_COLOR)
                lcm_target = lcm_start + RIGHT * (len(lcm_terms)) * 1.1
                self.play(copy.animate.move_to(lcm_target, aligned_edge=LEFT), run_time=0.5)
                self.wait(1.0)
                lcm_terms.append(f"({x_factors_list[i]})")
                lcm_val_new = MathTex(" \\cdot ".join(lcm_terms), color=LCM_COLOR, font_size=FONT_SIZE).move_to(lcm_start, aligned_edge=LEFT)
                self.play(FadeOut(copy), FadeOut(obj), Transform(lcm_val, lcm_val_new))
                self.wait(0.1)
        for j, used in enumerate(used_y):
            if not used:
                obj = y_objs[j]
                copy = obj.copy().set_color(LCM_COLOR)
                lcm_target = lcm_start + RIGHT * (len(lcm_terms)) * 1.1
                self.play(copy.animate.move_to(lcm_target, aligned_edge=LEFT), run_time=0.5)
                self.wait(1.0)
                lcm_terms.append(f"({y_factors_list[j]})")
                lcm_val_new = MathTex(" \\cdot ".join(lcm_terms), color=LCM_COLOR, font_size=FONT_SIZE).move_to(lcm_start, aligned_edge=LEFT)
                self.play(FadeOut(copy), FadeOut(obj), Transform(lcm_val, lcm_val_new))
                self.wait(0.1)

        # Fade out the top before solving GCF and LCM
        self.play(
            FadeOut(x_num), FadeOut(y_num),
            FadeOut(x_underline), FadeOut(y_underline),
            FadeOut(x_factors_tex), FadeOut(y_factors_tex)
        )
        self.wait(0.5)

        # Multiply out and show result (while GCF and LCM are still on screen)
        gcf_value = 1
        for t in gcf_terms[1:]:
            gcf_value *= int(t.strip("()"))
        lcm_value = 1
        for t in lcm_terms[1:]:
            lcm_value *= int(t.strip("()"))

        gcf_solved = MathTex(str(gcf_value), color=COMMON_COLOR, font_size=FONT_SIZE).move_to(gcf_val, aligned_edge=LEFT)
        lcm_solved = MathTex(str(lcm_value), color=LCM_COLOR, font_size=FONT_SIZE).move_to(lcm_val, aligned_edge=LEFT)
        self.play(
            Transform(gcf_val, gcf_solved),
            Transform(lcm_val, lcm_solved)
        )
        self.wait(1.0)

        # Fade out gcf/lcm values and labels before showing sentence
        self.play(
            FadeOut(gcf_val), FadeOut(lcm_val),
            FadeOut(gcf_label), FadeOut(lcm_label),
        )
        self.wait(0.5)

        summary = Tex(
            f"The GCF of {x} and {y} is {gcf_value} and LCM of {x} and {y} is {lcm_value}.",
            font_size=FONT_SIZE
        ).move_to(ORIGIN)
        self.play(Write(summary))
        self.wait(2)