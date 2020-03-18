% Classe com modelo de documento para listas de exercícios e provas.
% Adapta a classe "exam" para mostrar o cabeçalho identificando:
% - instituição
% - departamento
% - disciplina - turma - documento
% - professor
%
% Criado por : Guilherme N. Ramos em 2011

\ProvidesClass{UnBExam}%

%---------- Definindo Opções ----------%
\LoadClass[a4paper,12pt]{exam}%

% ---------- Pacotes ---------- %
\RequirePackage[brazilian]{babel}%	   Português
\RequirePackage[utf8]{inputenc}%  	   Arquivo em UTF8
\RequirePackage[T1]{fontenc}%          Fonte com caracteres acentuados
\RequirePackage{lmodern}%              Gera PDF "copiável" com o pdflatex.
\RequirePackage{graphicx} %			   Marca da UnB
\RequirePackage[top=15mm,
				bottom=15mm,
				left=15mm,
				right=15mm]{geometry}% Formatação do papel

% ---------- Comandos ---------- %
\newcommand{\universidade}[1]{\def\universidade@UnBExam{#1}}%
\newcommand{\departamento}[1]{\def\departamento@UnBExam{#1}}%
\newcommand{\disciplina}[1]{\def\disciplina@UnBExam{#1}}%
\newcommand{\turma}[1]{\def\turma@UnBExam{#1}}%
\newcommand{\professor}[2][Prof.]{\def\professor@UnBExam{\ifx#2\@empty\else#1 #2\fi}}%

\newcommand{\documento}[1]{\def\documento@UnBExam{#1}}%
\newcommand{\subdoc}[1]{\def\subdoc@UnBExam{#1}}%
\newcommand{\periodo}[1]{\def\periodo@UnBExam{#1}}%
\newcommand{\data}[1]{\def\data@UnBExam{#1}}%

% Inicialização
\universidade{\textbf{Universidade de Brasília}}%
\departamento{Departamento de Ciência da Computação}%
\disciplina{}%
\turma{}%
\professor{}%
\documento{}%
\subdoc{}%
\data{}%
\ifnum\month<3%
    \periodo{\the\year/0}%
\else\ifnum\month<8%
    \periodo{\the\year/1}%
\else%
    \periodo{\the\year/2}%
\fi\fi%

\newcommand{\identificacao@UnBExam}{%
	\ifx\disciplina@UnBExam\@empty%
	\else%
		\disciplina@UnBExam%
		 \ifx\turma@UnBExam\@empty\\%
		 \else\ - Turma \turma@UnBExam\\%
		 \fi%
	\fi%
	\ifx\documento@UnBExam\@empty\else\documento@UnBExam\\\fi%
}%

% ---------- Estilo ---------- %
\newenvironment{resposta}[1][]%
{%
	\ifx#1\@empty\else\renewcommand{\solutiontitle}{\noindent\textbf{#1:}\enspace}\fi%
	\setlength{\parskip}{0pt}%
	\ifprintanswers\vspace{-5mm}%
	\else\vspace{-10mm}%
	\fi
	\begin{EnvFullwidth}%
	\begin{solution}%
}%
{%
	\end{solution}%
	\end{EnvFullwidth}%
}%

\pagestyle{head}% every page to have a header but no footer

\let\@oldprintanswers=\printanswers%
\renewcommand{\printanswers}{\@oldprintanswers\extraheadheight[4cm]{0mm}}%

% Ajustes a classe Exam
\pointformat{{\small [\textbf{\themarginpoints}]}}%
\noprintanswers%
\pointsinmargin%
\renewcommand{\solutiontitle}{}%

% ---------- Definições ---------- %
\ifprintanswers%
\else%
	\extraheadheight[52mm]{0mm}%
\fi%

\newcommand{\nomeMatricula}{%
	\begin{tabular}{| p{.2\textwidth} | p{.75\textwidth} |}%
		\hline%
		\textbf{Matrícula} & \textbf{Nome}\\\hline%
		& \\ \hline%
	\end{tabular}
}%

\newcommand{\outrasInformacoes}{%
	\emph{Escreva seu nome e matrícula a caneta em todas as folhas. A compreensão
	do enunciado de cada questão também está sendo avaliada.}%
}%

\firstpageheader{%
	\begin{minipage}[c]{.6\textwidth}%
		\includegraphics[height=3em]{CIC_header}%
	\end{minipage}%
	\hfill%
	\begin{tabular}{r}%
		\ifx\data@UnBExam\@empty\else\small\data@UnBExam\fi\\%
		\ifx\periodo@UnBExam\@empty\else\small\periodo@UnBExam\fi%
	\end{tabular}%
	\begin{center}%
		\Large\textbf{\identificacao@UnBExam}%
	\end{center}%
	\hfill\ifx\professor@UnBExam\@empty\else\textit{\professor@UnBExam}\\\fi%
	\ifprintanswers%
		{%\large\vspace{-1\baselineskip}%
		\ifx\subdoc@UnBExam\@empty\else\hfill\textbf{\subdoc@UnBExam}\hfill\fi}%
	\else%
		\nomeMatricula\\%
		\outrasInformacoes%
	\fi%
}{}{}%
