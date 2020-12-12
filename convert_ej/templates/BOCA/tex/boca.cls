\NeedsTeXFormat{LaTeX2e}[1999/12/01]%

\ProvidesClass{boca}[2020/05/12 Formatacao de problemas/contests para o juiz eletronico BOCA.]%

\DeclareOption{notes}{\def\notes@boca{1}}%
\DeclareOption{tutorial}{\def\tutorial@boca{1}}%
\ProcessOptions\relax%

\LoadClass[12pt]{article}

% Packages
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
\setlength{\@inputWidth}{.475\textwidth}%
\setlength{\@outputWidth}{\@inputWidth}%
% \setlength{\@outputWidth}{\textwidth}%
% \addtolength{\@outputWidth}{-\@inputWidth}%

% Auxiliary commands
\newcommand{\@exampleCell}[1]{%
	\vspace{-1em}%
	\verbatiminput{#1}%
	\vspace{-2em}\vspace*{-0em}%
}%

\newcommand{\@iotable}[2]{%
	\noindent%
	\begin{tabular}[t]{p{\@inputWidth}|p{\@outputWidth}}%
		\ifodd\the@example\rowcolor{gray!20}\fi%
		#1 & #2%
	\end{tabular}%

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

\newcounter{@problem}%
\newcommand{\problem}[1]{%
	\stepcounter{@problem}%
	\newpage%
	\graphicspath{{#1/}}%

	\begin{center}%
	\large{\textbf{Problema~\Alph{@problem}}}%
	\\%
	\LARGE{\textbf{\input{#1/title}}}%
	\\%
	\footnotesize{Limite de tempo: \input{#1/time_limit}s}%
	\end{center}%

	\input{#1/description}%

	\section*{Entrada}%
	\input{#1/input}%

	\section*{Saída}%
	\input{#1/output}%

	\section*{Exemplos}%
	\@tabelasDeExemplos{#1}%

	\ifcsname notes@boca\endcsname
		\section*{Observações}%
		\input{#1/notes}%
	\fi%

	\ifcsname tutorial@boca\endcsname
		\section*{Tutorial}%
		\input{#1/tutorial}%
	\fi%
}%

\endinput%