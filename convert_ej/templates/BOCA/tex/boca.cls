\NeedsTeXFormat{LaTeX2e}[1999/12/01]%

\ProvidesClass{boca}[2020/05/12 Formatacao de problemas/contests para o juiz eletronico BOCA.]%

\DeclareOption{notes}{\def\notes@boca{1}}%
\DeclareOption{tutorial}{\def\tutorial@boca{1}}%
\ProcessOptions\relax%

\LoadClass[12pt]{article}

% Packages
\usepackage{amsmath}%
\usepackage{catchfile}%
\usepackage[margin=0.5in]{geometry}%
\usepackage{graphicx}%
\usepackage{ifthen}%
\usepackage[utf8]{inputenc}%
\usepackage{pgffor}%
\usepackage{verbatim}%
\usepackage[table]{xcolor}%

% Auxiliary settings
\newlength{\@inputWidth}%
\newlength{\@outputWidth}%

% Auxiliary commands
\newcommand{\@exampleCell}[1]{%
	\vspace{-1em}%
	\verbatiminput{#1}%
	\vspace{-2em}\vspace*{-0em}%
}%

\newcommand{\@iotable}[2]{%
	\noindent%
	\begin{tabular}[t]{p{.95\@inputWidth}|p{.95\@outputWidth}}%
		\ifodd\the@example\rowcolor{gray!20}\fi%
		#1 & #2%
	\end{tabular}%

}%

\newcommand{\@setInputWidth}[1]{%
	\setlength{\@inputWidth}{#1}%
	\setlength{\@outputWidth}{\textwidth}%
	\addtolength{\@outputWidth}{-#1}%
}%

% One table per example (verbatim input, highlighted rows)
\newcounter{@example}%
\newcommand{\@tabelasDeExemplos}[1]{%
	\CatchFileEdef{\examplelist}{#1/examples.csv}{\endlinechar=-1}%

	\@iotable{\textbf{Entrada}}{\textbf{Saída}}%
	\vspace*{0em}%

	\foreach \ex in \examplelist {
		\stepcounter{@example}%
		\@iotable{\@exampleCell{#1/../input/\ex}}{\@exampleCell{#1/../output/\ex}}%
	}
}%

\newcounter{problemCounter}%
\newcommand{\problem}[2][.5\textwidth]{%
	\stepcounter{problemCounter}%
	\newpage%
	\graphicspath{{#2/}}%

	\begin{center}%
	\large{\textbf{Problema~\Alph{problemCounter}}}%
	\\%
	\LARGE{\textbf{\input{#2/title}}}%
	\\%
	\footnotesize{Limite de tempo: \input{#2/time_limit}s}%
	\end{center}%

	\input{#2/description}%

	\section*{Entrada}%
	\input{#2/input}%

	\section*{Saída}%
	\input{#2/output}%

	\section*{Exemplos}%
	\setcounter{@example}{0}%
	\@setInputWidth{#1}%
	\@tabelasDeExemplos{#2}%

	\ifcsname notes@boca\endcsname
		\section*{Observações}%
		\input{#2/notes}%
	\fi%

	\ifcsname tutorial@boca\endcsname
		\section*{Tutorial}%
		\input{#2/tutorial}%
	\fi%
}%

\endinput%