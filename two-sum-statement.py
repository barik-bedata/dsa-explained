from manim import *
import numpy as np

config.flush_cache = True

# ═══════════════════════════════════════════════════════════════════
#  CourseTheme
# ═══════════════════════════════════════════════════════════════════
class CourseTheme:

    # ── raw palette (name-mangled = inaccessible outside class) ──
    __BG         = "#121212"
    __BLUE       = "#1A73E8"
    __GREEN      = "#198754"
    __RED        = "#DC3545"
    __YELLOW     = "#EAB308"
    __ORANGE     = "#F97316"
    __WHITE      = "#E0E0E0"
    __GRAY       = "#424242"
    __PURE_WHITE = "#FFFFFF"   # text on dark/blue/red/green fills
    __PURE_BLACK = "#000000"   # text on yellow/bright fills

    # ── typography & sizes ───────────────────────────────────────
    __FONT_UI   = "Inter"
    __FONT_CODE = "Fira Code"
    __FS_TITLE  = 52
    __FS_BODY   = 32
    __FS_LABEL  = 24
    __FS_SMALL  = 20
    __STROKE    = 2.5   # 2px–3px per spec for crisp 480p+ video

    # ── NEW: Scene Title & Dot variables ─────────────────────────
    __DOT_RADIUS        = 0.18       # অপটিমাইজড সাইজ
    __DOT_COLOR         = __WHITE    
    __SCENE_TITLE_SIZE  = 32         
    __SCENE_TITLE_COLOR = __WHITE    

    # ── background ───────────────────────────────────────────────
    def bg(self)              -> str:   return self.__BG

    # ── node/element colors ──────────────────────────────────────
    def node_blue(self)       -> str:   return self.__BLUE
    def node_green(self)      -> str:   return self.__GREEN
    def node_red(self)        -> str:   return self.__RED
    def node_yellow(self)     -> str:   return self.__YELLOW
    def node_orange(self)     -> str:   return self.__ORANGE
    def node_white(self)      -> str:   return self.__WHITE
    def node_gray(self)       -> str:   return self.__GRAY

    # ── text colors (per spec rules) ─────────────────────────────
    def text_on_dark(self)    -> str:   return self.__PURE_WHITE
    def text_on_yellow(self)  -> str:   return self.__PURE_BLACK
    def text_white(self)      -> str:   return self.__WHITE
    def text_gray(self)       -> str:   return self.__GRAY

    # ── typography & sizes ───────────────────────────────────────
    def font(self)             -> str:  return self.__FONT_UI
    def font_code(self)        -> str:  return self.__FONT_CODE
    def font_size_title(self)  -> int:  return self.__FS_TITLE
    def font_size_body(self)   -> int:  return self.__FS_BODY
    def font_size_label(self)  -> int:  return self.__FS_LABEL
    def font_size_small(self)  -> int:  return self.__FS_SMALL
    def stroke_width(self)     -> float: return self.__STROKE

    # ── NEW: Scene Title & Dot Getters ───────────────────────────
    def dot_radius(self)        -> float: return self.__DOT_RADIUS
    def dot_color(self)         -> str:   return self.__DOT_COLOR
    def scene_title_size(self)  -> int:   return self.__SCENE_TITLE_SIZE
    def scene_title_color(self) -> str:   return self.__SCENE_TITLE_COLOR


# ═══════════════════════════════════════════════════════════════════
#  CourseAnimator
# ═══════════════════════════════════════════════════════════════════
class CourseAnimator:

    def __init__(self, scene: Scene, theme: CourseTheme = None):
        self.__scene = scene
        self.__t     = theme if theme else CourseTheme()
        self.__scene.camera.background_color = self.__t.bg()

    # ── public interface ─────────────────────────────────────────

    def play_intro(self, title: str, subtitle: str = ""):
        t1, t2 = self.__build_intro(title, subtitle)
        self.__anim_intro(t1, t2)

    def play_section_title(self, section: str, number: int = 0):
        n, s, l = self.__build_section_title(section, number)
        self.__anim_section_title(n, s, l)

    def play_callout(self, text: str, position=None):
        if position is None:
            position = DOWN * 1.5
        box, label = self.__build_callout(text, position)
        self.__anim_callout(box, label)

    def play_lower_third(self, name: str, role: str = ""):
        bar, nm, rm = self.__build_lower_third(name, role)
        self.__anim_lower_third(bar, nm, rm)

    def play_outro(self, message: str = "See you in the next lesson!"):
        mob = self.__build_outro(message)
        self.__anim_outro(mob)

    def clear_screen(self, run_time: float = 0.6):
        if self.__scene.mobjects:
            self.__scene.play(
                *[FadeOut(m) for m in self.__scene.mobjects],
                run_time=run_time
            )

    # ── private builders ─────────────────────────────────────────

    def __build_intro(self, title, subtitle):
        t = self.__t
        title_mob = Text(title, font=t.font(),
                         font_size=t.font_size_title(),
                         color=t.node_blue(), weight=BOLD
                         ).move_to(UP * 0.4)
        sub_mob = (
            Text(subtitle, font=t.font(),
                 font_size=t.font_size_small(),
                 color=t.text_white())
            .next_to(title_mob, DOWN, buff=0.35)
        ) if subtitle else VMobject()
        return title_mob, sub_mob

    def __build_section_title(self, section, number):
        t = self.__t
        num_mob = Text(f"{number:02d}" if number else "",
                       font=t.font(), font_size=80,
                       color=t.node_yellow(), weight=BOLD
                       ).move_to(LEFT * 3)
        sec_mob = Text(section, font=t.font(),
                       font_size=t.font_size_body(),
                       color=t.text_white()
                       ).move_to(RIGHT * 1.2)
        line = Line(LEFT * 0.2 + UP * 1.5, LEFT * 0.2 + DOWN * 1.5,
                    color=t.node_blue(), stroke_width=t.stroke_width())
        return num_mob, sec_mob, line

    def __build_callout(self, text, position):
        t = self.__t
        label = Text(text, font=t.font(),
                     font_size=t.font_size_label(),
                     color=t.text_on_dark()
                     ).move_to(position)
        box = SurroundingRectangle(
            label, color=t.node_yellow(),   # YELLOW = active attention
            buff=0.25, corner_radius=0.12,
            stroke_width=t.stroke_width()
        )
        return box, label

    def __build_lower_third(self, name, role):
        t = self.__t
        bar = Rectangle(width=config.frame_width, height=0.9,
                        fill_color=t.node_blue(), fill_opacity=0.92,
                        stroke_width=0).to_edge(DOWN, buff=0)
        nm  = Text(name, font=t.font(), font_size=30,
                   color=t.text_on_dark(), weight=BOLD
                   ).move_to(bar.get_center() + LEFT * 3 + UP * 0.05)
        rm  = (
            Text(role, font=t.font(),
                 font_size=t.font_size_small(),
                 color=t.text_on_dark())
            .next_to(nm, RIGHT, buff=0.5)
        ) if role else VMobject()
        return bar, nm, rm

    def __build_outro(self, message):
        t = self.__t
        return Text(message, font=t.font(),
                    font_size=t.font_size_body(),
                    color=t.node_green()     # GREEN = success / lesson complete
                    ).move_to(ORIGIN)

    # ── private animators ────────────────────────────────────────

    def __anim_intro(self, title_mob, sub_mob):
        self.__scene.play(Write(title_mob, run_time=1.2))
        if isinstance(sub_mob, Text):
            self.__scene.play(FadeIn(sub_mob, shift=UP * 0.2, run_time=0.8))
        self.__scene.wait(1.5)

    def __anim_section_title(self, num_mob, sec_mob, line):
        self.__scene.play(
            FadeIn(num_mob, shift=RIGHT * 0.4, run_time=0.6),
            GrowFromCenter(line, run_time=0.5),
        )
        self.__scene.play(Write(sec_mob, run_time=0.8))
        self.__scene.wait(1.2)

    def __anim_callout(self, box, label):
        self.__scene.play(Create(box, run_time=0.5), Write(label, run_time=0.6))
        self.__scene.wait(1.8)

    def __anim_lower_third(self, bar, nm, rm):
        bar.shift(DOWN * bar.height)
        self.__scene.add(bar)
        self.__scene.play(bar.animate.shift(UP * bar.height), run_time=0.5)
        self.__scene.play(
            Write(nm, run_time=0.6),
            FadeIn(rm, run_time=0.5) if isinstance(rm, Text) else Wait(0),
        )
        self.__scene.wait(2)
        self.__scene.play(FadeOut(bar), FadeOut(nm), FadeOut(rm), run_time=0.4)

    def __anim_outro(self, mob):
        self.__scene.play(FadeIn(mob, run_time=0.8))
        self.__scene.wait(1.5)
        self.__scene.play(FadeOut(mob, run_time=1.2))


# ═══════════════════════════════════════════════════════════════════
#  Two Sum Statement Scene
# ═══════════════════════════════════════════════════════════════════
class Statement(Scene):
    def construct(self):
        # থিম ইনিশিয়ালাইজ করা হলো
        theme = CourseTheme()
        
        # ১. প্রিমিয়াম ম্যাট অফ-ব্ল্যাক ব্যাকগ্রাউন্ড 
        self.camera.background_color = theme.bg() 

        # ==========================================
        # ২. LAYOUT SETUP (Title with Dot, Array with Label, Target)
        # ==========================================
        
        # টপ-লেফট কর্নারে ক্লিন টাইটেল (থিম থেকে সাইজ ও কালার নেওয়া হয়েছে)
        title_text = Text(
            "Two Sum", 
            font=theme.font(), 
            font_size=theme.scene_title_size(), 
            color=theme.scene_title_color()
        )
        
        # সাদা ডট (থিম থেকে রেডিয়াস এবং কালার নেওয়া হয়েছে)
        dot = Circle(
            radius=theme.dot_radius(), 
            color=theme.dot_color(), 
            fill_opacity=1, 
            stroke_width=0
        )
        
        # ডট এবং টেক্সটকে একটি VGroup-এ রাখা হলো এবং টেক্সটের সাথে সেন্টার-অ্যালাইন করা হলো
        title_group = VGroup(dot, title_text).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        
        # পুরো গ্রুপটিকে টপ-লেফট কর্নারে পজিশন করা হলো
        title_group.to_edge(UP + LEFT, buff=0.5)
        self.add(title_group)

        # বামপাশের "nums = " লেবেল (কোড ফন্ট)
        nums_label = Text("nums = ", font=theme.font_code(), font_size=theme.font_size_label(), color=theme.text_white())
        
        # জিরো-গ্যাপ মেমোরি অ্যারে
        nums = [2, 1, 3, 5, 8]
        array_cells = VGroup(*[
            VGroup(
                Square(side_length=1.0, color=theme.node_gray(), stroke_width=theme.stroke_width(), fill_opacity=0),
                Text(str(val), font=theme.font_code(), font_size=theme.font_size_label(), color=theme.text_white())
            ) for val in nums
        ]).arrange(buff=0)
        
        # স্ক্রিনের ডেড স্পেস কমাতে অ্যারে উইন্ডোকে UP * 0.6 পজিশনে ওপরে তোলা হলো
        array_with_label = VGroup(nums_label, array_cells).arrange(RIGHT, buff=0.25)
        array_with_label.move_to(LEFT * 2.0 + UP * 0.6)
        
        # বক্সগুলো ওপরে সেটেল হওয়ার পর তাদের মাথার ওপর পারফেক্টলি ইনডেক্স প্লেস করা হলো
        indices = VGroup(*[
            Text(str(idx), font=theme.font_code(), font_size=theme.font_size_small(), color=theme.text_gray())
            .next_to(array_cells[idx][0], UP, buff=0.15)
            for idx in range(len(nums))
        ])
        
        # পুরো কমপ্লিট লেফট গ্রুপ
        left_content = VGroup(array_with_label, indices)

        # ডানপাশের মডার্ন টার্গেট ক্যাপসুল
        target_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.9, color=theme.node_gray(), stroke_width=theme.stroke_width(), fill_opacity=0)
        target_txt = Text("Target = 9", font=theme.font(), font_size=theme.font_size_label(), color=theme.text_white())
        right_target_group = VGroup(target_box, target_txt).move_to(RIGHT * 4.2 + UP * 0.6)

        # স্ক্রিনে লেআউট লোড হওয়া
        self.play(
            FadeIn(title_group, shift=RIGHT * 0.3),
            FadeIn(left_content, shift=RIGHT * 0.3),
            FadeIn(right_target_group, shift=LEFT * 0.3),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # ==========================================
        # ৩. SELECTION PHASE (Yellow Border -> Blue Processing Fill)
        # ==========================================
        
        cell_1 = array_cells[1]
        cell_4 = array_cells[4]
        
        # নোড দুটিকে লেয়ারের সামনে আনা হলো যেন বর্ডার গ্লিচ না করে
        self.bring_to_front(cell_1, cell_4)
        
        # স্কয়ারের বর্ডার ইয়েলো (Active Focus) হবে
        self.play(
            cell_1[0].animate.set_stroke(color=theme.node_yellow(), width=6),
            cell_4[0].animate.set_stroke(color=theme.node_yellow(), width=6),
            run_time=0.7,
            rate_func=smooth
        )
        
        # ব্যাকগ্রাউন্ড ব্লু (Processing) ফিল হবে এবং টেক্সট অন-ডার্ক (সাদা) হবে
        self.play(
            cell_1[0].animate.set_fill(theme.node_blue(), opacity=1),
            cell_4[0].animate.set_fill(theme.node_blue(), opacity=1),
            cell_1[1].animate.set_color(theme.text_on_dark()),
            cell_4[1].animate.set_color(theme.text_on_dark()),
            Flash(cell_1[0], color=theme.node_yellow(), flash_radius=0.7, num_lines=12, line_stroke_width=theme.stroke_width()),
            Flash(cell_4[0], color=theme.node_yellow(), flash_radius=0.7, num_lines=12, line_stroke_width=theme.stroke_width()),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.6)

        # ==========================================
        # ৪. SUMMATION PHASE (Values Move Down & Replace with Sum)
        # ==========================================
        
        val1_copy = cell_1[1].copy()
        val2_copy = cell_4[1].copy()
        
        calc_y_pos = -1.4
        plus_sign = Text("+", font=theme.font_code(), font_size=theme.font_size_label(), color=theme.text_white()).move_to(np.array([0, calc_y_pos, 0]))
        
        self.play(
            val1_copy.animate.next_to(plus_sign, LEFT, buff=0.4),
            val2_copy.animate.next_to(plus_sign, RIGHT, buff=0.4),
            FadeIn(plus_sign),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.5)
        
        equation_group = VGroup(val1_copy, plus_sign, val2_copy)
        
        sum_box = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.6, color=theme.node_gray(), stroke_width=theme.stroke_width(), fill_opacity=0)
        sum_txt = Text("9", font=theme.font_code(), font_size=theme.font_size_label(), color=theme.text_white())
        sum_card = VGroup(sum_box, sum_txt).move_to(np.array([0, calc_y_pos, 0]))
        
        self.play(
            ReplacementTransform(equation_group, sum_card),
            run_time=0.8
        )
        self.wait(0.6)

        # ==========================================
        # ৫. FINAL REPLACEMENT (Green Success Box & Flying Indices)
        # ==========================================
        
        # থিমের রুলস অনুযায়ী ফাইনাল সাকসেসের জন্য গ্রিন কালার
        final_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=0.8, color=theme.node_green(), stroke_width=4, fill_opacity=0)
        final_box.move_to(np.array([0, calc_y_pos, 0]))
        
        final_txt = Text("[1, 4]", font=theme.font_code(), font_size=theme.font_size_label(), color=theme.text_white()).move_to(final_box.get_center())
        
        idx1_flying_copy = indices[1].copy()
        idx4_flying_copy = indices[4].copy()
        
        self.bring_to_front(idx1_flying_copy, idx4_flying_copy)
        
        # ম্যাজিক ট্র্যান্সফর্ম: সংখ্যা '9' চলে যাবে, এবং ইনডেক্স দুটি উড়ে এসে ব্র্যাকেটে লক হবে
        self.play(
            ReplacementTransform(sum_box, final_box),
            FadeOut(sum_txt),
            FadeIn(final_txt[0]), # '['
            FadeIn(final_txt[2]), # ','
            FadeIn(final_txt[4]), # ']'
            ReplacementTransform(idx1_flying_copy, final_txt[1]), 
            ReplacementTransform(idx4_flying_copy, final_txt[3]),
            run_time=1.6,
            rate_func=smooth
        )
        
        # ফাইনাল সাকসেস ফ্ল্যাশ (Green) এবং অ্যারো সেলগুলোও Green হয়ে যাওয়া
        self.play(
            Flash(final_box, color=theme.node_green(), flash_radius=1.0, num_lines=16, line_stroke_width=4),
            cell_1[0].animate.set_fill(theme.node_green()).set_stroke(theme.node_green()),
            cell_4[0].animate.set_fill(theme.node_green()).set_stroke(theme.node_green()),
            run_time=0.5
        )
        self.wait(3)